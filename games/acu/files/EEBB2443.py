from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader
import numpy


@register_file_reader('EEBB2443')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):

        BaseFile.__init__(self, file_id)
        file.read_bytes(2)
        file.read_file_id()

        for _ in range(3):
            file.read_file()
        file.read_numpy(numpy.float32, 16)
        file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')

        file.read_file()
        file.read_bytes(1)
        file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')
