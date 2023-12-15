from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x43EF99C2
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(15)  # previously 17
        file.out_file_write('\n')

        """
        01 00 00 00 00 00 00 00 00 00 00 00 00 00 00 01 00 00 00
        00 00 80 3F 00 00 7A 44 00 00 A0 41 CD CC 4C 3D CD CC CC 3D 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        """

        """
        01 00 00 00 00 00 00 00 00 00 00 00 00 00 00
        trmMtx
        """
