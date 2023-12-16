from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xB0438131
    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()
        file.read_bytes(count1)
