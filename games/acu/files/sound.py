from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x83EC6C6D
    def read(self, file_id: int, file: FileDataWrapper):
        type_id_or_something = file.read_uint_32()
        assert 0 <= file.read_uint_8() <= 1, "check byte should be 0 or 1"
        file_name_size = file.read_uint_32()
        if file_name_size:
            file_name = file.read_bytes(file_name_size)
            assert file.read_uint_8() == 0, "check byte should be 0"
        # assert file.read_uint_8() == 0, "check byte should be 0"

        # more stuff after this
        # file.read_bytes(34)
        # count1 = file.read_uint_32()
        # for _ in range(count1):
        #     file.read_bytes(1)
        #     file.read_file()
