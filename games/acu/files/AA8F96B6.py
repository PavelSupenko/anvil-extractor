from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xAA8F96B6
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(11)
        for _ in range(5):
            file.read_float_32()
        file.read_bytes(10)
        # file.read_bytes(1)
        file.out_file_write('\n')
