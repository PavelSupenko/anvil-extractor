import importlib
import inspect
import pkgutil

from model.files.base_file import BaseFile
from model.files.file_readers_factory_base import FileReadersFactoryBase


class AC1FileReadersFactory(FileReadersFactoryBase):
    def __init__(self):
        file_readers_map = get_file_readers_types_map()
        super().__init__(file_readers_map)


def get_file_readers_types_map() -> dict[int, type]:
    package_name = __name__

    # Initialize an empty list to store instances of subclasses of BaseFile
    # Usage: from type_readers import instances
    file_readers: dict[int, type] = {}

    # Iterate through all modules in the current package
    for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
        if not is_pkg:  # If it's a package, continue the iteration
            module = importlib.import_module(f"{package_name}.{module_name}")
            for name, obj in inspect.getmembers(module):
                if inspect.isclass(obj) and issubclass(obj, BaseFile) and obj != BaseFile:
                    # If the object is a subclass of BaseFile and not BaseFile itself
                    file_readers[obj.ResourceType] = obj  # Add the instance to the list

    return file_readers
