from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x414FF9F7
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(1)
        count1 = file.read_uint_32()
        for _ in range(count1):
            file.read_bytes(2)
            file.read_file_id()
            file.read_resource_type()
            file.read_bytes(4)
            file.out_file_write('\n')
        file.out_file_write('\n')
