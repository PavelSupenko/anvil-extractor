from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x0E2F4444
    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()
        count2 = file.read_uint_32()

        for _ in range(count2):
            file.read_file()
