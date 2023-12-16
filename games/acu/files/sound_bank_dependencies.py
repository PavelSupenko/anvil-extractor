from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x1B478101
    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()
        with file.indent:
            for _ in range(count1):
                file.read_bytes(1)
                file.read_file()  # 6290D74A SoundBank
