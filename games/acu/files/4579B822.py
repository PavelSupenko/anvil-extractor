from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x4579B822
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_float_32()
        file.read_bytes(20)
