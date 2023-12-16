from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from games.acu.files.entity import Reader as Entity


class Reader(BaseFile):
    ResourceType = 0xD77FB524

    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(2)
        self.entity: Entity = file.read_file()
        count1 = file.read_uint_32()
        file.indent()
        for _ in range(count1):
            file.read_file()
        file.indent(-1)
        count2 = file.read_uint_32()
        file.indent()
        file.read_bytes(4 * count2)
        file.indent(-1)
        file.read_uint_32()  # coord 1
        file.read_uint_32()  # coord 2
        file.read_bytes(1)
