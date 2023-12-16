from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x71FDA747
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(4)
        file.read_file_id()
        file.read_bytes(33)
