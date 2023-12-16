from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x35363B17
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(2)
        for _ in range(7):
            file.read_file()
