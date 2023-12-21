import os

from model.export.export_plugin_base import ExportPluginBase
from model.export.mtl.mtl_object import ObjMtl
from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from model.files.file_readers_factory_base import FileReadersFactoryBase
from model.files.mesh import BaseMesh
from model.files.texture import BaseTexture
from model.forge.forge_data import ForgeData
from model.forge.forge_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportMeshPlugin(ExportPluginBase):
    target_type = '415D9568'
    file_type_int = 0x415D9568
    texture_type_int = 0xA2B7E917
    plugin_name = 'Export Mesh'

    def __init__(self, output_directory_path: str, file_readers_factory: FileReadersFactoryBase):
        super().__init__(output_directory_path, file_readers_factory)

    def execute_internal(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], forge_data: ForgeData,
                         file_id, file_data: ForgeFileData, game_data: GameData):
        self.forge_reader = forge_reader
        self.forge_readers = forge_readers
        self.forge_data = forge_data
        self.file_id = file_id
        self.file_data = file_data
        self.game_data = game_data

        file_name = file_data.name

        file_bytes = forge_reader.get_decompressed_files_bytes(file_data)
        file_path = os.path.join(self.output_directory_path, game_data.name)

        print(f'Exporting mesh data to {file_path}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        reader = self.file_readers_factory.get_file_reader(self.file_type_int)
        material_reader = self.file_readers_factory.get_file_reader(0x85C817C3)
        texture_set_reader = self.file_readers_factory.get_file_reader(0xD70E6670)

        # Not needed because method export_mesh_dds is a full copy of Reader functionality
        # texture_reader = self.file_readers_factory.get_file_reader(0xA2B7E917)

        reader_file: BaseFile = reader
        mesh: BaseMesh = reader

        bytes = file_bytes[file_id]
        file: FileDataWrapper = FileDataWrapper(bytes, game_data)

        reader_file.read(file_id, file)

        obj_handler = ObjMtl(file_name, file_path, forge_reader, forge_readers, forge_data, file_id, file_data, game_data,
                             material_reader, texture_set_reader)
        obj_handler.export(mesh, file_name)
        obj_handler.save_and_close(self.export_mesh_dds)
        print(f'Exported {file_id:016X}')

    def export_mesh_dds(self, file_id, save_folder: str):
        forge_reader = self.forge_reader

        if file_id not in forge_reader.forge_data.files_data:
            for forge_reader_another in self.forge_readers:
                if file_id in forge_reader_another.forge_data.files_data:
                    forge_reader = forge_reader_another
                    break

        file_data = forge_reader.forge_data.files_data[file_id]
        file_bytes = forge_reader.get_decompressed_files_bytes(file_data)
        file_path = os.path.join(self.output_directory_path, self.game_data.name,
                                 f'{file_data.name}.dds')

        print(f'Exporting texture data to {file_path}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        reader = self.file_readers_factory.get_file_reader(self.texture_type_int)
        reader_file: BaseFile = reader
        reader_texture: BaseTexture = reader

        bytes = file_bytes[file_id]
        file: FileDataWrapper = FileDataWrapper(bytes, self.game_data)

        reader_file.read(file_id, file)
        reader_texture.export_dds(file_path)

        # Used inside MtlObject to write texture path to .mtl file
        return file_path
