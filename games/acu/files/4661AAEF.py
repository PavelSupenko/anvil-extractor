from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x4661AAEF
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(2)
        count1 = file.read_uint_32()
        file.read_bytes(2 * count1)
        file.read_bytes(4 * 6)  # 6 floats
        count2 = file.read_uint_32()
        for _ in range(count2):
            file.read_bytes(24)
        file.read_bytes(1)
        file.out_file_write('\n')
