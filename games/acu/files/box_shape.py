from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x4EC68E98
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_struct('5f')
        file.read_struct('16f')
        file.read_bytes(10)
