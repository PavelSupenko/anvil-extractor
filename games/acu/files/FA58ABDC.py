from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xFA58ABDC
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(10)
        file.read_file_id()
        file.read_bytes(23)
        for _ in range(3):
            file.read_bytes(2)
            file.read_file_id()
