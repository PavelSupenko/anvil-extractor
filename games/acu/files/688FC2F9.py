from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x688FC2F9
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(4)
        file.read_file_id()
