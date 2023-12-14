from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('D3F7FFC8')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id)
        file.read_bytes(4)
        count = file.read_uint_32()
        for _ in range(count):
            file.indent()
            file.read_bytes(2)
            file.indent(-1)
            file.read_file()
        file.read_bytes(4)
