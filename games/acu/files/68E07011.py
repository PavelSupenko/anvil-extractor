from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x68E07011
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)
