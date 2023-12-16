from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x2DCC1F56
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(5)
        file.read_file_id()
        file.read_bytes(10)
