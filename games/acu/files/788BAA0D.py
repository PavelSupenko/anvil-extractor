from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x788BAA0D
    def read(self, file_id: int, file: FileDataWrapper):
        for _ in range(4):
            for _ in range(4):
                file.read_float_32()
        file.out_file_write('\n')
