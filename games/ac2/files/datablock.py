from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xAC2BBF68
    def read(self, file_id: int, file: FileDataWrapper):
        count1 = file.read_uint_32()
        self.files = []
        for _ in range(count1):
            file.read_bytes(2)  # 0100 as a delimiter
            self.files.append(file.read_file_id())
        file.out_file_write('\n')
        count2 = file.read_uint_32()  # seems to be about the same or slightly less than count1
        self.cell_id = file.read_uint_32()
