from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x7F57D331
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(16)
        something = file.read_bytes(4)
        while something != b'\x14\x10\x67\x4C':
            file.read_bytes(16)
            something = file.read_bytes(4)
        file.read_bytes(49)
