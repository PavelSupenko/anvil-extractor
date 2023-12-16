from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x5730D30E

    def read(self, file_id: int, file: FileDataWrapper):
        file.read_file()

        count1 = file.read_uint_32()
        for _ in range(count1):
            file.read_bytes(12)

        count2 = file.read_uint_32()
        if count2 != 0:
            raise Exception()
