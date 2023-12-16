from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x94CCDC09
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(33)
        for _ in range(file.read_uint_32()):
            assert file.read_uint_8() == 0, "check byte failed"
            file.read_file_id()

        for _ in range(file.read_uint_32()):
            str_len = file.read_uint_32()
            name = file.read_bytes(str_len)
            assert file.read_uint_8() == 0, "check byte failed"
