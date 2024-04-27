from pydantic import BaseModel
import importlib
import inspect
import pkgutil


class FunctionModel(BaseModel):
    name: str


class LibraryWrapper(BaseModel):
    package: object
    functions: list[FunctionModel] = []

    def __init__(self, package_name: str, **kwargs):
        super().__init__(package=importlib.import_module(package_name), **kwargs)
        self._load_functions()

    def _load_functions(self):
        for importer, modname, ispkg in pkgutil.iter_modules(self.package.__path__):
            module = importlib.import_module(f"{self.package.__name__}.{modname}")
            for func_name, func in inspect.getmembers(module, inspect.isfunction):
                self.functions.append(FunctionModel(name=func_name))

    def __getattr__(self, name):
        for func in self.functions:
            if func.name == name:
                module_name, func_name = name.rsplit(".", 1)
                module = importlib.import_module(
                    f"{self.package.__name__}.{module_name}"
                )
                return getattr(module, func_name)
        raise AttributeError(f"'LibraryWrapper' object has no attribute '{name}'")


# Example usage:
library_wrapper = LibraryWrapper(package_name="PittAPI")

# Now you can access all the functions from the package as attributes of the class
print(library_wrapper.schema_json(indent=2))
# Assuming get_course_sections is a function in the package
# print(library_wrapper.get_course_sections())
