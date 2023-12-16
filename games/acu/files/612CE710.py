from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x612CE710
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_uint_32()
        for _ in range(file.read_uint_32()):
            with file.indent:
                file.read_file()
