from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x2E8B5553
    def read(self, file_id: int, file: FileDataWrapper):
        # file.read_bytes(2)
        file.out_file_write('\n')
