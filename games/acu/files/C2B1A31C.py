from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xC2B1A31C
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(4)
        file.read_float_32()
        file.read_bytes(1)
        count = file.read_uint_32()
        for n in range(count):
            file.read_file()
        file.read_bytes(1)
        file.read_file()
        file.read_bytes(26)
        file.read_file_id()
        file.read_bytes(8)
