from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x81A7045D

    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(9)
        file.read_file_id()
        file.read_bytes(17)
        for _ in range(18):
            file.read_file()
