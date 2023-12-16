from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xFFA6D96A
    def read(self, file_id: int, file: FileDataWrapper):
        count = file.read_uint_32()
        for _ in range(count):
            file.read_file()
