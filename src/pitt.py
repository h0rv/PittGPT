import inspect
import pkgutil
from inspect import isfunction, signature
from typing import get_type_hints

import PittAPI
import pydantic
from pydantic.main import BaseModel


class Pitt(BaseModel):
    ...


def get_pitt_model() -> Pitt:
    functions = []
    for loader, module_name, is_pkg in pkgutil.walk_packages(
        PittAPI.__path__, PittAPI.__name__ + "."
    ):
        module = loader.find_module(module_name).load_module(module_name)
        for member_name in dir(module):
            member = getattr(module, member_name)
            if inspect.isfunction(member) and not member_name.startswith("_"):
                module_name_stripped = module_name.removeprefix("PittAPI.")
                member.__name__ = f"{module_name_stripped}.{member.__name__}"
                functions.append(member)

    func_defs = {}
    for func in functions:
        if not isfunction(func):
            continue
        sig = signature(func)
        type_hints = get_type_hints(func)

        field_definitions = {}
        for param in sig.parameters.values():
            arg_name = param.name
            type_hint = type_hints.get(arg_name, pydantic.Field(None))
            default_value = param.default if param.default is not param.empty else ...
            field_definitions[arg_name] = (type_hint, default_value)

        # Add function docstring to field definitions
        field_definitions["description"] = (str, func.__doc__)

        func_defs[func] = field_definitions

    args = {
        func.__name__: (pydantic.create_model(func.__name__, **fields), ...)
        for func, fields in func_defs.items()
    }

    model = pydantic.create_model(
        "Pitt",
        **args,
    )

    return model


def get_pitt_json_schema() -> str:
    p = get_pitt_model()
    return p.schema_json()
