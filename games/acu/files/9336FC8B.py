from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x9336FC8B
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(8 * 4)  # FFF0FFF0
        count1 = file.read_uint_32()
        self.count = count1
        if count1 == 0:
            pass
        elif 0 < count1 < 100000:
            file.indent()
            file.read_bytes(count1 * 4)
            file.indent(-1)
        else:
            raise Exception('Probably an issue here')
        count2 = file.read_uint_32()
        if count2 == 0:
            pass
        elif 0 < count2 < 100000:
            file.indent()
            file.read_bytes(count2)
            file.indent(-1)
            file.read_bytes(2)  # \x03\x03
        else:
            raise Exception('Probably an issue here')
