from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('5730D30E')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):

        BaseFile.__init__(self, file_id)
        file.read_file()

        count1 = file.read_uint_32()
        for _ in range(count1):
            file.read_bytes(12)

        count2 = file.read_uint_32()
        if count2 != 0:
            raise Exception()
