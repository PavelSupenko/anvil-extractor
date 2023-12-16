from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x0B6FBC0D

    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(8)
        for _ in range(8):
            file.read_float_32()
        file.read_bytes(16)
