import os

from model.export.export_plugin_base import ExportPluginBase
from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from model.files.file_readers_factory_base import FileReadersFactoryBase
from model.files.texture import BaseTexture
from model.forge.forge_data import ForgeData
from model.forge.forge_container_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportTexturePlugin(ExportPluginBase):
    target_type = 'A2B7E917'
    file_type_int = 0xA2B7E917
    plugin_name = 'Export DDS'

    def __init__(self, output_directory_path: str, file_readers_factory: FileReadersFactoryBase):
        super().__init__(output_directory_path, file_readers_factory)

    def execute_internal(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], forge_data: ForgeData,
                         file_id, file_data: ForgeFileData, game_data: GameData):

        file_bytes = forge_reader.get_decompressed_files_bytes(file_data)
        file_path = os.path.join(self.output_directory_path, game_data.name,
                                     f'{file_data.name}_{file_id:016X}.dds')

        print(f'Exporting texture data to {file_path}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        reader = self.file_readers_factory.get_file_reader(self.file_type_int)
        reader_file: BaseFile = reader
        reader_texture: BaseTexture = reader

        bytes = file_bytes[file_id]
        file: FileDataWrapper = FileDataWrapper(bytes, game_data)

        reader_file.read(file_id, file)
        reader_texture.export_dds(file_path)
