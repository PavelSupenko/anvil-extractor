from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x3939DC9A
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)  # 00
        file.read_file()  # 8A2588E8
