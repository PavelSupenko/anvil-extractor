from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import numpy


class Reader(BaseFile):
    ResourceType = 0x228F402A
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_file()
        file.read_file_id()
        file.read_bytes(2)
        file.read_bytes(17)
        file.out_file_write('Transformation Matrix\n')
        self.transformation_matrix = file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')
