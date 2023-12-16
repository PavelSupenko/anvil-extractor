from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x9E1CD34A
    def read(self, file_id: int, file: FileDataWrapper):
        count = file.read_uint_32()
        # for _ in range(count):  # the above looks like a count but there is only 1 of the below
        file.read_file()
