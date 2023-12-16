from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xECEF6DDB
    def read(self, file_id: int, file: FileDataWrapper):
        count2 = file.read_uint_32()
        for _ in range(count2):
            file.read_file()
