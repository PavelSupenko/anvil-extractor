
from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x92BC18F7
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(7)
