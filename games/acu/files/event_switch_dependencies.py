from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x43F19E3B
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        header = file.read_bytes(21)  # all 00
        count = file.read_uint_8()
        for _ in range(count):
            file.read_bytes(5)
            file.read_file()
        assert all(b == 0 for b in header), "expected header to be all 00"
