from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('939B245D')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id)
        file.read_bytes(22)
        file.read_file()  # gameplay surface nav type
        count = file.read_uint_32()
        for _ in range(count):
            file.read_file()
        file.read_bytes(22)
        file.read_float_32()
        file.read_file()
        file.read_bytes(39)
