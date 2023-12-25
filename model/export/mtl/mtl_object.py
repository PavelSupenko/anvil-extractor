import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from typing import Union, List, Callable

import numpy

from model.export.mtl.material_handler import MaterialHandler
from model.files.file_readers_factory_base import FileReadersFactoryBase
from model.files.mesh import BaseMesh
from model.forge.forge_data import ForgeData
from model.forge.forge_container_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ObjMtl:
    """This is a handler to export to the OBJ format with and MTL file for materials
    This model exporter works by writing the mesh data for each mesh directly to the file as it is given it. (using the .export method).
	These models should be pre-manipulated as the values are directly written.
	While this is being done the materials are saved to a buffer.
	When the .save_and_close method is called these materials are written to the mtl file.
	"""

    def __init__(self, model_name: str, save_folder: str, forge_reader: ForgeReader, forge_readers: list[ForgeReader],
                 forge_data: ForgeData, file_id, file_data: ForgeFileData, game_data: GameData,
                 file_readers_factory: FileReadersFactoryBase):

        self.missing_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources', 'MissingTexture.png')
        self.missing_name = os.path.basename(self.missing_path)

        self.forge_readers = forge_readers
        self.forge_reader = forge_reader
        self.forge_data = forge_data
        self.file_id = file_id
        self.file_data = file_data

        self.model_name = model_name
        self.save_folder = save_folder
        self.vertex_count = 0  # the number of vertices that have been processed. Used to calculate the vertex offset
        self.mtl_handler = MaterialHandler(forge_reader, forge_readers, forge_data, file_id, file_data, game_data,
                                           file_readers_factory)  # used when generating the .mtl file
        self._group_name = {}  # used for getting a unique name for each model
        self.missing_no_exported = False

        # the obj file object
        if not os.path.isdir(self.save_folder):
            os.makedirs(self.save_folder)
        self._obj = open(f'{self.save_folder}{os.sep}{self.model_name}.obj', 'w')
        self._obj.write(
            '# Wavefront Object File\n# Exported by Anvil Extractor based on ACExplorer, written by gentlegiantJGC, and ARchive_neXt\n\n')
        self._obj.write(f'mtllib ./{self.model_name}.mtl\n')

    def group_name(self, name: str) -> str:
        """
		Each model in the obj needs to have a unique name. When this is called a unique name will be returned
		:return: '{self.name}_{int}'
		"""
        if name not in self._group_name:
            self._group_name[name] = -1
        self._group_name[name] += 1
        return f'{name}_{self._group_name[name]}'

    def export(self, model: BaseMesh, model_name: str,
               transformation_matrix: Union[List[numpy.ndarray], numpy.ndarray] = None) -> None:
        """
		when called will export the currently loaded mesh to the obj file
		when finished will reset all the mesh variables so that things do not persist
		:return: None
		"""
        if isinstance(transformation_matrix, numpy.ndarray) and transformation_matrix.shape == (4, 4):
            vertices = numpy.vstack((model.vertices.transpose(), numpy.ones((1, model.vertices.shape[0]))))
            # vertices[:3, :] *= 0.001
            vertices = numpy.dot(transformation_matrix, vertices)[:3, :].transpose()
        else:
            vertices = model.vertices
        # write vertices
        self._obj.write(('v {} {} {}\n' * vertices.shape[0]).format(*vertices.ravel().round(6)))
        self._obj.write(f'# {len(model.vertices)} vertices\n\n')

        # write texture coords
        self._obj.write(
            ('vt {} {}\n' * model.texture_vertices.shape[0]).format(*model.texture_vertices.ravel().round(6)))
        self._obj.write(f'# {len(model.texture_vertices)} texture coordinates\n\n')

        # write faces
        for mesh_index, mesh in enumerate(model.meshes):
            self._obj.write(f'g {self.group_name(model_name)}\nusemtl {self.mtl_handler.get(model.materials[mesh_index]).name}\n')
            self._obj.write(('f {}/{} {}/{} {}/{}\n' * mesh['face_count']).format(*numpy.repeat(model.faces[mesh_index][:mesh['face_count']], 2).astype(numpy.int_) + self.vertex_count + 1))
            self._obj.write(f'# {mesh["face_count"]} faces\n\n')

        self.vertex_count += len(model.vertices)

    def save_and_close(self, export_dds_handler: Callable[[int, str], str]) -> None:
        """
		when called will create the mtl file and write its contents
		when finished will close both mtl and self._obj
		:return:
		"""
        if not os.path.isdir(self.save_folder):
            os.makedirs(self.save_folder)
        mtl = open(f'{self.save_folder}{os.sep}{self.model_name}.mtl', 'w')
        mtl.write(
            '# Material Library\n# Exported by Anvil Extractor based on ACExplorer, written by gentlegiantJGC, and ARchive_neXt\n\n')

        with ThreadPoolExecutor(max_workers=10) as executor:
            fild_ids = [
                file_id
                for
                material in self.mtl_handler.materials.values()
                if not material.missing_no for
                map_type, file_id in [
                    ['map_Kd', material.diffuse],
                    ['map_d', material.diffuse],
                    ['map_Ks', material.specular],
                    ['map_bump', material.normal],
                    ['disp', material.height]
                ]
                if file_id is not None
            ]
            materials = list(executor.map(
                export_dds_handler,
                fild_ids,
                [self.save_folder] * len(fild_ids)
            ))

        material_counter = 0
        for material in self.mtl_handler.materials.values():
            mtl.write(f'newmtl {material.name}\n')
            mtl.write('Ka 1.000 1.000 1.000\nKd 1.000 1.000 1.000\nKs 0.000 0.000 0.000\nNs 0.000\n')

            if material.missing_no:
                mtl.write(f"map_Kd {self.missing_name}\n")
                self.export_missing_no()
            else:
                for map_type, file_id in [
                    ['map_Kd', material.diffuse],
                    ['map_d', material.diffuse],
                    ['map_Ks', material.specular],
                    ['map_bump', material.normal],
                    ['disp', material.height]
                ]:
                    if file_id is not None:
                        image_path = materials[material_counter]
                        material_counter += 1
                        if image_path is None:
                            mtl.write(f"{map_type} {self.missing_name}\n")
                            self.export_missing_no()
                        else:
                            mtl.write(f'{map_type} {os.path.basename(image_path)}\n')
            mtl.write('\n')
        mtl.close()
        self._obj.close()

    def export_missing_no(self) -> None:
        """
        Call this to copy over the missingNo image if it has not already been copied over
        :return: None
        """
        if not self.missing_no_exported:
            self.missing_no_exported = True
            shutil.copy(self.missing_path, self.save_folder)
