from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x24AECB7C
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(4)
        count = file.read_uint_32()
        self.bones = []
        for _ in range(count):
            assert file.read_uint_8() == 0, "Check byte failed"
            self.bones.append(
                file.read_file()
            )

        if file.read_uint_8() == 2:
            file.read_bytes(66)
            if file.read_uint_8() != 3:
                assert file.read_uint_8() == 0, "Check byte failed"
                file.read_file()
            file.read_bytes(8)
