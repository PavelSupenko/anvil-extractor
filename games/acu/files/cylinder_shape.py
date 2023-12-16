from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x445B37F9
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_struct('5f')
        file.read_struct('5f')
        file.read_bytes(10)
