from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('F49B6117')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id)
        file.read_bytes(1)
        for _ in range(4):
            file.read_bytes(4)
        count1 = file.read_uint_32()
        for _ in range(count1):
            file.read_bytes(2)
            file.read_file_id()
