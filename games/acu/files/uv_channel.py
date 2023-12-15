from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xBDAD8273
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(5)
        for n in (8, 4):
            count = file.read_uint_32()
            with file.indent:
                file.read_bytes(count * n)
