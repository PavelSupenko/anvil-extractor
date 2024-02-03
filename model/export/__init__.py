import importlib
import inspect
import pkgutil

from model.export.export_plugin_base import ExportPluginBase
from model.files.file_readers_factory_base import FileReadersFactoryBase


class ExportPluginsFactory:

    def __init__(self, output_directory: str, file_readers_factory_base: FileReadersFactoryBase):
        self.output_directory = output_directory
        self.file_readers_factory_base = file_readers_factory_base

    def get(self, file_type: str) -> list[ExportPluginBase]:
        # Get the current package name
        package_name = __name__

        # Initialize an empty list to store instances of subclasses of ExportPluginBase
        # Usage: from type_readers import instances
        default_export_plugins = []

        # Iterate through all modules in the current package
        for loader, module_name, is_pkg in pkgutil.walk_packages(__path__):
            if not is_pkg:  # If it's a package, continue the iteration
                module = importlib.import_module(f"{package_name}.{module_name}")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, ExportPluginBase) and obj != ExportPluginBase:
                        if obj.target_type == file_type or obj.target_type == '*':
                            # If the object is a subclass of ExportPluginBase and not ExportPluginBase itself
                            # Create an instance of the class
                            instance = obj(self.output_directory, self.file_readers_factory_base)

                            is_plugin_already_in_array: bool = False
                            for plugin_in_array in default_export_plugins:
                                if plugin_in_array.plugin_name == instance.plugin_name:
                                    is_plugin_already_in_array = True

                            if not is_plugin_already_in_array:
                                default_export_plugins.append(instance)  # Add the instance to the list

        return default_export_plugins
