from typing import Any, Iterable, List

from PittAPI import (
    course,
    dining,
    lab,
    laundry,
    library,
    news,
    people,
    shuttle,
    textbook,
)
from pydantic import BaseModel, ConfigDict, Field

from pitt import get_pitt_json_schema


class Arg(BaseModel):
    name: str = Field(description="name of the function argument")
    value: Any = Field(description="value of the function argument")

    def __str__(self) -> str:
        return f"{self.name}={self.value}"


class Function(BaseModel):
    name: str  # TODO make literal containing all function names
    args: List[Arg]

    model_config = ConfigDict(
        json_schema_extra={"avaiable_functions": [get_pitt_json_schema()]}
        # json_schema_extra={"avaiable_functions": [pitt.model_json_schema()]}
    )

    def __str__(self) -> str:
        args_str = ", ".join([str(arg) for arg in self.args])
        return f"{self.name}({args_str})"


def functions_handler(funcs: Iterable[Function]) -> None:
    for func in funcs:
        try:
            func_str = str(func)
            print(f"Running:\n  `{func_str}`")

            result = exec(func_str)
            print(f"{func_str} = {result}")
        except Exception as e:
            print("Error occurred during execution:", e)
