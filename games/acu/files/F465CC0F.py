from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xF465CC0F
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):

        BaseFile.__init__(self, file_id, file)
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(5)
        count = file.read_uint_32()  # zero
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(17)
        count2 = file.read_uint_32()
        for _ in range(count2):
            file.indent()
            file.read_bytes(1)
            file.read_file()
            file.indent(-1)
