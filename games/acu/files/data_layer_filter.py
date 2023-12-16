from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xDB1D406E
    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()  # count
        # more data follows this if count != 0
        for _ in range(count1):
            file.read_file()
        file.out_file_write('\n')
