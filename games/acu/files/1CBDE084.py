from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import numpy


class Reader(BaseFile):
    ResourceType = 0x1CBDE084

    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(2)
        file.read_file_id()
        file.out_file_write('\n')

        for _ in range(2):
            file.read_file()

        self.transformation_matrix = file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')
        file.out_file_write('\n')

        count1 = file.read_uint_32()

        self.files = []

        for _ in range(count1):
            file.read_bytes(1)
            self.files.append(
                file.read_file_id()
            )
        file.out_file_write('\n')
