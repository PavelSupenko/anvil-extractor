from abc import ABC

from model.files.file_readers_factory_base import FileReadersFactoryBase
from model.forge.forge_data import ForgeData
from model.forge.forge_container_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportPluginBase(ABC):
    target_type = ''
    plugin_name = ''

    def __init__(self, output_directory_path: str, file_readers_factory: FileReadersFactoryBase):
        self.output_directory_path = output_directory_path
        self.file_readers_factory = file_readers_factory

    def execute(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], file_data: ForgeFileData, game_data: GameData):
        forge_data: ForgeData = forge_reader.forge_data
        file_id = file_data.id

        print(f'Exporting using plugin: {self.plugin_name} for file: {file_id} to directory: {self.output_directory_path}')

        if file_id not in forge_data.files_data:
            print(f'File ID {file_id} not found in forge data')
            return

        file_data: ForgeFileData = forge_data.files_data[file_id]
        print(f'File name: {file_data.name}, type: {file_data.type}, id: {file_data.id}')

        self.execute_internal(forge_reader, forge_readers, forge_data, file_id, file_data, game_data)

    def execute_internal(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], forge_data: ForgeData,
                         file_id, file_data: ForgeFileData, game_data: GameData):
        raise NotImplementedError()
