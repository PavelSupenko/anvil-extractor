from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xD0C34A81
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(5)
        count = file.read_uint_32()
        file.read_bytes(1)
        for _ in range(count):
            file.read_file()
        file.read_bytes(16)
