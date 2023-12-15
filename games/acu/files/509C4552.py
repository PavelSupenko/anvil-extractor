from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x509C4552
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(8)
        file.read_bytes(4 * 4)  # 4 floats
        file.read_bytes(4)
        file.out_file_write('\n')
