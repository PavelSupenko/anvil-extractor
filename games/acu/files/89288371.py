from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x89288371
    def read(self, file_id: int, file: FileDataWrapper):
        for _ in range(2):
            file.read_file()
        file.read_bytes(1)
