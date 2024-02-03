import os
from functools import partial
from operator import is_not

import numpy

from model.export.export_plugin_base import ExportPluginBase
from model.export.mtl.mtl_object import ObjMtl
from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from model.files.file_readers_factory_base import FileReadersFactoryBase
from model.files.mesh import BaseMesh
from model.files.texture import BaseTexture
from model.forge.forge_data import ForgeData
from model.forge.forge_container_file_data import ForgeFileData, ForgeContainerFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportEntityPlugin(ExportPluginBase):
    target_type = '984415E'
    file_type_int = 0x0984415E

    texture_type_int = 0xA2B7E917
    mesh_data_type_int = 0x415D9568

    plugin_name = 'Export Entity'

    def __init__(self, output_directory_path: str, file_readers_factory: FileReadersFactoryBase):
        super().__init__(output_directory_path, file_readers_factory)

    def create_mesh_data_reader(self):
        return self.file_readers_factory.get_file_reader(self.mesh_data_type_int)

    def execute_internal(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], forge_data: ForgeData,
                         file_id, file_data: ForgeFileData,  container_file_data: ForgeContainerFileData, game_data: GameData):
        file_name = file_data.name

        file_bytes = forge_reader.get_decompressed_files_bytes(container_file_data)
        file_path = os.path.join(self.output_directory_path, game_data.name)

        print(f'Exporting mesh data to {file_path}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        reader = self.file_readers_factory.get_file_reader(self.file_type_int)

        entity: BaseFile = reader

        bytes = file_bytes[file_id]
        file: FileDataWrapper = FileDataWrapper(bytes, game_data)

        entity.read(file_id, file)

        if entity is None or entity.nested_files is None:
            print(f"Failed reading entity file {file_name} with id {file_id} ({file_id:016X})")
            return

        obj_handler = ObjMtl(file_name, file_path, forge_reader, forge_readers, forge_data, file_id, file_data,
                             game_data, self.file_readers_factory)

        entity_nested_files: list[BaseFile] = entity.nested_files
        valid_entity_nested_files: list[BaseFile] = list(filter(partial(is_not, None), entity_nested_files))
        visual_resource_files: list[BaseFile] = list(
            filter(lambda x: x.resource_type == 0xEC658D29, valid_entity_nested_files))

        for visual_file in visual_resource_files:
            # visual_file: Visual
            if 0x01437462 in visual_file.nested_files.keys():  # LOD selector
                # lod_selector: LODSelector = visual_file.nested_files[0x01437462]
                # mesh_instance_data: MeshInstanceData = lod_selector[self._options[0]['LOD']]
                lod_selector = visual_file.nested_files[0x01437462]
                mesh_instance_data = lod_selector[0]  # 0 is a lod level
            elif 0x536E963B in visual_file.nested_files.keys():  # Mesh instance
                # mesh_instance_data: MeshInstanceData = visual_file.nested_files[0x536E963B]
                mesh_instance_data = visual_file.nested_files[0x536E963B]
            else:
                print(f"Could not find mesh instance data for {file_name} {file_id} ({file_id:016X})")
                continue

            if mesh_instance_data is None:
                print(f"Failed to find mesh data inside entity: {file_name}")
                continue

            mesh_file_data, mesh_file_bytes = self.find_forge_container_file_data(mesh_instance_data.mesh_id)
            if mesh_file_data is None:
                print(f"Failed to find file {mesh_instance_data.mesh_id} ({mesh_instance_data.mesh_id:016X})")
                continue

            reader_file: BaseFile = self.create_mesh_data_reader()
            mesh: BaseMesh = reader_file

            mesh_file: FileDataWrapper = FileDataWrapper(mesh_file_bytes, game_data)
            reader_file.read(mesh_file_data.id, mesh_file)

            if mesh is None or mesh.vertices is None:
                print(f"Failed reading model file {mesh_file_data.name} {mesh_file_data.id} ({mesh_file_data.id:016X})")
                continue

            transform = entity.transformation_matrix
            if len(mesh_instance_data.transformation_matrix) == 0:
                # here is the problem with incorrect transform!
                obj_handler.export(mesh, mesh_file_data.name)
            else:
                for trm in mesh_instance_data.transformation_matrix:
                    obj_handler.export(mesh, mesh_file_data.name, numpy.matmul(transform, trm))
            print(f'Exported {mesh_file_data.name}')

        obj_handler.save_and_close(self.export_mesh_dds)
        print(f'Finished exporting {file_name}.obj')

    def export_mesh_dds(self, file_id, save_folder: str):
        file_data, bytes = self.find_forge_container_file_data(file_id)
        file_path = os.path.join(self.output_directory_path, self.game_data.name,
                                 f'{file_data.name}.dds')

        print(f'Exporting texture data to {file_path}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        reader = self.file_readers_factory.get_file_reader(self.texture_type_int)
        reader_file: BaseFile = reader
        reader_texture: BaseTexture = reader

        file: FileDataWrapper = FileDataWrapper(bytes, self.game_data)

        reader_file.read(file_id, file)
        reader_texture.export_dds(file_path)

        # Used inside MtlObject to write texture path to .mtl file
        return file_path
