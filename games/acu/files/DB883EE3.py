from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xDB883EE3
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(2)  # 01 00
        file.read_file()  # 3939DC9A
