from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xDF5D6C0E
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(44)
        for _ in range(3):
            file.read_file()
