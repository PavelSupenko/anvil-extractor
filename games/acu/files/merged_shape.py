from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import numpy
import logging


class Reader(BaseFile):
    ResourceType = 0x2D675BA2

    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()  # possibly a count
        if count1 != 0:
            logging.warning('"2D675BA2" count1 is not 0')
        count2 = file.read_uint_32()
        for _ in range(count2):
            file.read_bytes(2)
            file.read_file_id()
        file.out_file_write('\n')
        count3 = file.read_uint_32()
        file.out_file_write('\n')
        self.transformation_matrix = []
        for _ in range(count3):  # transformation matrix
            self.transformation_matrix.append(file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F'))
            file.out_file_write('\n')

        count4 = file.read_uint_32()
        file.out_file_write('\n')
        for _ in range(count4):
            file.read_file()
        file.out_file_write('\n')
