import grequests
import PittAPI
import pkgutil
import inspect
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module="grequests")


# Iterate over the modules in the PittAPI package
for loader, module_name, is_pkg in pkgutil.walk_packages(
    PittAPI.__path__, PittAPI.__name__ + "."
):
    # Import the module
    module = loader.find_module(module_name).load_module(module_name)

    # Print the module name
    print(f"Module:")
    print(f"  {module_name}")
    print(f"  Functions:")

    # Iterate over the members of the module
    for member_name in dir(module):
        member = getattr(module, member_name)

        # Check if the member is a function
        if inspect.isfunction(member) and not member_name.startswith("_"):
            signature = inspect.signature(member)
            args = []
            for param in signature.parameters.values():
                arg_name = param.name
                arg_type = (
                    param.annotation.__name__
                    if param.annotation != param.empty
                    else "unknown"
                )
                args.append(f"{arg_name}: {arg_type}")

            docstring = inspect.getdoc(member)
            if docstring:
                print(f"    {member_name}  ({', '.join(args)})")
                print(f"       {docstring}")
            else:
                print(f"    {member_name}")

    print()
