from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x13237FE9
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(48)
        file.read_bytes(file.read_uint_32())
