from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xF4833172
    def read(self, file_id: int, file: FileDataWrapper):
        for _ in range(2):
            assert file.read_uint_8() == 0, "check byte failed"
            file.read_file()
