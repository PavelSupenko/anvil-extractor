from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xBC300CF6
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(2)
        count = file.read_uint_32()
        for _ in range(count):
            file.read_bytes(2)
            file.read_file()
        file.read_struct('8f')
        file.read_bytes(1)
