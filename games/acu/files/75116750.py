from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('75116750')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id)
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(5)
        count = file.read_uint_32()
        file.read_bytes(1)
        for _ in range(count):
            file.indent()
            file.read_file()
            file.indent(-1)
        file.read_bytes(16)
