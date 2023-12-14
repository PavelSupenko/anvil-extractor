import os

from model.export.export_plugin_base import ExportPluginBase
from model.forge.forge_data import ForgeData
from model.forge.forge_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportFormatPlugin(ExportPluginBase):
    file_type = '*'
    plugin_name = 'Export Format'

    def __init__(self, output_directory_path: str):
        super().__init__(output_directory_path)

    def execute_internal(self, forge_reader: ForgeReader, forge_data: ForgeData, file_id,
                         file_data: ForgeFileData, game_data: GameData):

        file_bytes = forge_reader.get_decompressed_files_bytes(file_data)
        file_path = os.path.join(self.output_directory_path, game_data.name, f'{file_data.name}_{file_id:016X}.format')

        print(f'Exporting binary data to {file_path}')

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        f = open(file_path, "w")
        # file_wrapper = FileFormatDataWrapper(file_bytes, self, f)

        print(file_bytes)
