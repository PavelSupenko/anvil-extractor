from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xC8C23780

    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(16)
        # three floats and zeros
        file.out_file_write('\n')
