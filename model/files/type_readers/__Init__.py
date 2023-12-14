import importlib
import inspect
import pkgutil

from model.files.reading.base_reader import BaseReader


def get_default_type_readers() -> list[BaseReader]:
    # Get the current package name
    package_name = __name__

    # Initialize an empty list to store instances of subclasses of BaseReader
    # Usage: from type_readers import instances
    default_type_readers = []

    # Iterate through all modules in the current package
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
        if not is_pkg:  # If it's a package, continue the iteration
            module = importlib.import_module(f"{package_name}.{module_name}")
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseReader) and obj != BaseReader:
                    # If the object is a subclass of BaseReader and not BaseReader itself
                    instance = obj()  # Create an instance of the class
                    default_type_readers.append(instance)  # Add the instance to the list

    return default_type_readers