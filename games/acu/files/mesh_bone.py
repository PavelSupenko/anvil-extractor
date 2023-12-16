import numpy

from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x9EF0E7A1
    def read(self, file_id: int, file: FileDataWrapper):
        self.bone_id = file.read_resource_type()  # bone name?
        # self.bone_name = pyUbiForge.game_functions.resource_types.get(self.bone_id, self.bone_id)
        self.transformation_matrix = file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')
        file.read_bytes(1)
