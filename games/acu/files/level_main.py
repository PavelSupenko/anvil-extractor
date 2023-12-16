from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xFBB63E47
    def read(self, file_id: int, file: FileDataWrapper):
        for _ in range(2):
            file.read_file()  # 7DB083ED  contains data block ids

        file.read_bytes(2)
        self.fakes = file.read_file_id()

        file.read_bytes(2)
        file.read_file_id()

        # sequence data table
        count = file.read_uint_32()
        with file.indent:
            for _ in range(count):
                file.read_bytes(2)
                file.read_file_id()

        file.read_bytes(2)
        file.read_file()

        assert file.read_uint_8() == 0, "check byte failed"
        file.read_file()
