from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x7DB083ED
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(26)
        check_byte = file.read_uint_8()
        if check_byte:
            file.read_file()
        else:
            file.read_bytes(4)  # 00 * 8 half which is probably the below but unsure which

        count3 = file.read_uint_32()
        file.read_bytes(count3 * 2)
