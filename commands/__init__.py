import os
import sys
import inspect
import importlib
from project import Project, require_project
from functools import wraps
from typing import Callable, Any

# The registry map where all functions are recorded
_registry: dict[str, Callable[..., Any]] = {}

def command(name: str):
    """Decorator to register a function as a runnable command line action."""
    def decorator(func: Callable[..., Any]):
        sig = inspect.signature(func)
        params = list(sig.parameters.values())

        needs_project = any(p.annotation == Project for p in params)

        target_func = require_project(func) if needs_project else func

        @wraps(func)
        def wrapper(path: str, args: list[str]) -> Any:
            bound_kwargs = {}
            args_pool = list(args)

            if needs_project:
                bound_kwargs["path"] = path

            for param in params:
                if param.annotation == Project:
                    continue

                elif param.name == "path":
                    bound_kwargs["path"] = path

                elif param.name == "args" and param.annotation == list[str]:
                    bound_kwargs[param.name] = args_pool
                    break

                elif args_pool:
                    bound_kwargs[param.name] = args_pool.pop(0)

            return target_func(**bound_kwargs)

        _registry[name] = wrapper
        return wrapper
    return decorator

def call(name: str, path: str, args: list[str]) -> Any:
    """Invokes a registered command by name, passing the path and remaining arguments."""
    if name not in _registry:
        print(f"Error: Unknown command '{name}'.", file=sys.stderr)
        sys.exit(1)

    return _registry[name](path, args)

_package_dir = os.path.dirname(__file__)

for _file in os.listdir(_package_dir):
    if _file.endswith(".py") and _file != "__init__.py":
        _module_name = _file[:-3]

        # Programmatically import the submodule relative to this package context
        importlib.import_module(f".{_module_name}", package=__name__)