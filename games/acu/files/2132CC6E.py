from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x2132CC6E
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(12)
        checkByte = file.read_bytes(1)
        file.read_file()
