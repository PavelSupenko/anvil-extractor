from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xD14C5C7E
    def read(self, file_id: int, file: FileDataWrapper):
        for _ in range(file.read_uint_32()):
            file.read_file()
