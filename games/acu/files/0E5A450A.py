from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x0E5A450A

    def read(self, file_id: int, file: FileDataWrapper):
        # readStr(fIn, fOut, 184)
        file.read_bytes(14)
        for _ in range(2):
            file.read_file()
        file.read_bytes(1)
        check_byte = file.read_uint_8()
        if check_byte != 3:
            file.read_file_id()
        count = file.read_uint_32()
        for _ in range(count):
            file.read_bytes(1)
            file.read_file_id()
        file.read_bytes(9)
