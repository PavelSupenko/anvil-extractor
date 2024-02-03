from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x995BFBF5
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(2)
        file.read_file_id()
        file.out_file_write('\n')
