from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x9060AB6E
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(72)
        file.read_file()
