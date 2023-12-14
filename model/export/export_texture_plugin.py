import os

from model.export.export_plugin_base import ExportPluginBase
from model.forge.forge_data import ForgeData
from model.forge.forge_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportTexturePlugin(ExportPluginBase):
    file_type = 'A2B7E917'
    plugin_name = 'Export DDS'

    def __init__(self, output_directory_path: str):
        super().__init__(output_directory_path)

    def execute_internal(self, forge_reader: ForgeReader, forge_data: ForgeData, file_id,
                         file_data: ForgeFileData, game_data: GameData):

        file_bytes = forge_reader.get_decompressed_files_bytes(file_data)
        print(file_bytes)

        for file_item_id, file_item_bytes in file_bytes.items():
            file_path = os.path.join(self.output_directory_path, game_data.name,
                                     f'{file_data.name}_{file_id:016X}', f'{file_item_id}.bin')

            print(f'Exporting binary data to {file_path}')
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            f = open(file_path, "wb")
            f.write(file_item_bytes)