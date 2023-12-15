from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x59327905
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        assert file.read_uint_8() == 0, "check byte failed"
        file.read_file_id()
        for _ in range(file.read_uint_32()):
            file.read_file()
        file.read_bytes(20)
