from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import numpy


class Reader(BaseFile):
    ResourceType = 0x4AEC3476
    def read(self, file_id: int, file: FileDataWrapper):
        self.bounding_box = file.read_numpy(numpy.float32, 24).reshape((3, 2))
        file.read_uint_32()
        file.out_file_write('\n')
