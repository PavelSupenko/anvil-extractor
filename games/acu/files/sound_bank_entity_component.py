from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xDAB4219F
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(3)
        file.read_file()  # 1B478101
