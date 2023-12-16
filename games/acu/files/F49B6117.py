from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xF49B6117
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)
        for _ in range(4):
            file.read_bytes(4)
        count1 = file.read_uint_32()
        for _ in range(count1):
            file.read_bytes(2)
            file.read_file_id()
