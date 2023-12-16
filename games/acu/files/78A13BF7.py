from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x78A13BF7
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(2)
        count = file.read_uint_32()
        for _ in range(count):
            file.read_file()  # 49FCD7BF
