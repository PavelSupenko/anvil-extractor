from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xAC2BBF68
    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()
        self.files = []
        for _ in range(count1):
            file.indent()
            file.read_bytes(2)
            self.files.append(file.read_file_id())
            file.indent(-1)
        file.out_file_write('\n')
        count2 = file.read_uint_32()  # seems to be about the same or slightly less than count1
        self.cell_id = file.read_uint_32()
        file.read_bytes(4)  # this might be part of the previous as a 64 bit uint
