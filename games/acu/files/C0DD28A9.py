from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xC0DD28A9
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(5)
        file.read_bytes(12)
        file.read_bytes(4 * 4 * 4 + 4)
        count = file.read_uint_32()
        for _ in range(count):
            file.indent()
            file.read_file()
            file.indent(-1)
