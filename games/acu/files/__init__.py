import importlib
import inspect
import pkgutil

from model.files.base_file import BaseFile


package_name = __name__

# Initialize an empty list to store instances of subclasses of BaseFile
# Usage: from type_readers import instances
file_reader_types = {}

# Iterate through all modules in the current package
for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
    if not is_pkg:  # If it's a package, continue the iteration
        module = importlib.import_module(f"{package_name}.{module_name}")
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj) and issubclass(obj, BaseFile) and obj != BaseFile:
                # If the object is a subclass of BaseFile and not BaseFile itself
                file_reader_types[obj.ResourceType] = obj # Add the instance to the list


def create_file_readers() -> BaseFile:
    file_reader_types[]

    instance = obj()  # Create an instance of the class

    return file_readers
