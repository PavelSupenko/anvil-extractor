from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x7313743E
    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()
        file.read_bytes(10)
        for _ in range(count1):
            file.read_file()
