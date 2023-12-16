from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xCF153BBA
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(1)
        file.read_file_id()  # same as the top level parent
        count = file.read_uint_32()
        assert count in (1, 3), "expected 1 or 3"
        file.read_numpy("float32", 396)
        if count == 1:
            file.read_bytes(1)
        elif count == 3:
            file.read_bytes(2)
