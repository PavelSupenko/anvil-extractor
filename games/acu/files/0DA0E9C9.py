from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x0DA0E9C9

    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(66)
        count = file.read_uint_32()
        for _ in range(count):
            file.read_file()
        file.read_bytes(33)  # 01 followed by 8 floats
