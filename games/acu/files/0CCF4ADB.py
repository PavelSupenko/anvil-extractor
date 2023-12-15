from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x0CCF4ADB

    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(4)
        file.read_file_id()
        file.read_bytes(1)
        file.read_file()
        file.read_bytes(1)

        file.out_file_write('\n')

        for _ in range(7):
            file.read_float_32()
        file.read_bytes(3)
