from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x49F4CA3E
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(5)
        for _ in range(2):
            check_byte = file.read_uint_8()
            if check_byte != 3:
                file.read_file_id()

        file.read_bytes(32)
