from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xD3156717
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_uint_8()
        file.read_file_id()
