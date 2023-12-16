from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x939B245D
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(22)
        file.read_file()  # gameplay surface nav type
        count = file.read_uint_32()
        for _ in range(count):
            file.read_file()
        file.read_bytes(22)
        file.read_float_32()
        file.read_file()
        file.read_bytes(39)
