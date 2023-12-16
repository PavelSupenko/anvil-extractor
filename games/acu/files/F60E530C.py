from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


# found just after sound stuff

class Reader(BaseFile):
    ResourceType = 0xF60E530C
    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()
        file.read_bytes(1)
        file.read_file()  # CF153BBA
