from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x4FB33274
    def read(self, file_id: int, file: FileDataWrapper):
        check = file.read_uint_8()
        if check == 1:
            file.read_bytes(3)
