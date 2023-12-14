from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('E6545731')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id)
        count1 = file.read_int_32()
        for _ in range(count1):
            file.read_bytes(2)
            file.read_file_id()
        file.out_file_write('\n')
        count2 = file.read_int_32()
        for _ in range(count2):
            file.read_bytes(2)
            file.read_file()
