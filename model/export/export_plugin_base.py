from abc import ABC

from model.forge.forge_data import ForgeData
from model.forge.forge_file_data import ForgeFileData


class ExportPluginBase(ABC):
    def __init__(self, target_type: str, plugin_name: str, output_directory_path: str):
        self._target_type = target_type
        self._plugin_name = plugin_name
        self.output_directory_path = output_directory_path

    @property
    def target_type(self) -> str:
        return self._target_type

    @property
    def plugin_name(self) -> str:
        return self._plugin_name

    def execute(self, forge_data: ForgeData, file_id):
        print(f'Exporting using plugin: {self.plugin_name} for file: {file_id} to directory: {self.output_directory_path}')

        if file_id not in forge_data.files_data:
            raise ValueError(f'File ID {file_id} not found in forge data')

        file_data: ForgeFileData = forge_data.files_data[file_id]
        print(f'File name: {file_data.name}, type: {file_data.type}, id: {file_data.id}')
        #raise NotImplementedError
