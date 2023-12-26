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


class ExportMeshPlugin(ExportPluginBase):
    target_type = 'AC2BBF68'
    file_type_int = 0xAC2BBF68

    texture_type_int = 0xA2B7E917
    entity_type_int = 0x0984415E
    mesh_data_type_int = 0x415D9568

    # texture_type_int = 0xA2B7E917
    plugin_name = 'Export Data Block'

    def __init__(self, output_directory_path: str, file_readers_factory: FileReadersFactoryBase):
        super().__init__(output_directory_path, file_readers_factory)

    def create_entyty_reader(self):
        return self.file_readers_factory.get_file_reader(self.entity_type_int)

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

        reader_file: BaseFile = reader

        bytes = file_bytes[file_id]
        file: FileDataWrapper = FileDataWrapper(bytes, game_data)

        reader_file.read(file_id, file)
        data_block_files = reader_file.files

        obj_handler = ObjMtl(file_name, file_path, forge_reader, forge_readers, forge_data, file_id, file_data,
                             game_data, self.file_readers_factory)

        for data_block_entry_id in data_block_files:
            entry_file_data, entry_file_bytes = self.find_forge_container_file_data(data_block_entry_id)

            if entry_file_data is None:
                print(f"Failed to find file {data_block_entry_id:016X}")
                continue

            if entry_file_data.type in (0x0984415E, 0x3F742D26):  # entity and entity group
                try:
                    entity: BaseFile = self.create_entyty_reader()
                    entity_file: FileDataWrapper = FileDataWrapper(entry_file_bytes, game_data)
                    entity.read(data_block_entry_id, entity_file)
                except Exception as exception:
                    print(f"Failed reading file {entry_file_data.name} {entry_file_data.id:016X}")
                    entity = None

                if entity is None or entity.nested_files is None:
                    print(f"Failed reading entity file {entry_file_data.name} {entry_file_data.id:016X}")
                    continue

                entity_nested_files: list[BaseFile] = entity.nested_files
                valid_entity_nested_files: list[BaseFile] = list(filter(partial(is_not, None), entity_nested_files))

                for nested_file in valid_entity_nested_files:
                    if nested_file.resource_type == 0xEC658D29:  # visual
                        # nested_file: Visual
                        if 0x01437462 in nested_file.nested_files.keys():  # LOD selector
                            # lod_selector: LODSelector = nested_file.nested_files[0x01437462]
                            # mesh_instance_data: MeshInstanceData = lod_selector[self._options[0]['LOD']]
                            lod_selector = nested_file.nested_files[0x01437462]
                            mesh_instance_data = lod_selector[0]  # 0 is a lod level
                        elif 0x536E963B in nested_file.nested_files.keys():  # Mesh instance
                            # mesh_instance_data: MeshInstanceData = nested_file.nested_files[0x536E963B]
                            mesh_instance_data = nested_file.nested_files[0x536E963B]
                        else:
                            print(f"Could not find mesh instance data for {entry_file_data.name} {entry_file_data.id:016X}")
                            continue
                        if mesh_instance_data is None:
                            print(f"Failed to find file {entry_file_data.name}")
                            continue
                        # model_data = pyUbiForge.temp_files(mesh_instance_data.mesh_id)

                        mesh_file_data, mesh_file_bytes = self.find_forge_container_file_data(mesh_instance_data.mesh_id)

                        if mesh_file_data is None:
                            print(f"Failed to find file {mesh_instance_data.mesh_id:016X}")
                            continue

                        reader_file: BaseFile = self.create_mesh_data_reader()
                        mesh: BaseMesh = reader_file

                        mesh_file: FileDataWrapper = FileDataWrapper(mesh_file_bytes, game_data)
                        reader_file.read(mesh_file_data.id, mesh_file)

                        if mesh is None or mesh.vertices is None:
                            print(f"Failed reading model file {mesh_file_data.name} {mesh_file_data.id:016X}")
                            continue
                        transform = entity.transformation_matrix
                        if len(mesh_instance_data.transformation_matrix) == 0:
                            obj_handler.export(mesh, mesh_file_data.name, transform)
                        else:
                            for trm in mesh_instance_data.transformation_matrix:
                                obj_handler.export(mesh, mesh_file_data.name, numpy.matmul(transform, trm))
                        print(f'Exported {mesh_file_data.name}')
            else:
                print(f'File type "{entry_file_data.type}" is not currently supported. It has been skipped')

        obj_handler.save_and_close(self.export_mesh_dds)
        print(f'Finished exporting {file_name}.obj')

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
