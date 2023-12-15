from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import numpy


class Reader(BaseFile):
    ResourceType = 0xEEBB2443
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):

        BaseFile.__init__(self, file_id, file)
        file.read_bytes(2)
        file.read_file_id()

        for _ in range(3):
            file.read_file()
        file.read_numpy(numpy.float32, 16)
        file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')

        file.read_file()
        file.read_bytes(1)
        file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')
