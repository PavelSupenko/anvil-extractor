import os

from model.export.export_plugin_base import ExportPluginBase
from model.files.file_data_wrapper import FileDataWrapper
from model.files.file_readers_factory_base import FileReadersFactoryBase
from model.forge.forge_data import ForgeData
from model.forge.forge_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportBinaryPlugin(ExportPluginBase):
    target_type = '*'
    plugin_name = 'Export Binary'

    def __init__(self, output_directory_path: str, file_readers_factory: FileReadersFactoryBase):
        super().__init__(output_directory_path, file_readers_factory)

    def execute_internal(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], forge_data: ForgeData,
                         file_id, file_data: ForgeFileData, game_data: GameData):
        file_bytes = forge_reader.get_decompressed_files_bytes(file_data)

        if file_bytes is None:
            print(f"Failed to find file {file_id:016X}")
            return

        file_path = os.path.join(self.output_directory_path, game_data.name,
                                 f'{file_data.name}_{file_id:016X}.bin')

        print(f'Exporting binary data to {file_path}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        bytes = file_bytes[file_id]
        file: FileDataWrapper = FileDataWrapper(bytes, game_data)

        out_file = open(file_path, 'wb')
        out_file.write(file.read_rest())
