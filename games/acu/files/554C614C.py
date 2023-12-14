from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('554C614C')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id)
        file.read_bytes(1)
        file.read_file_id()
        file.read_bytes(2)
        file.out_file_write('\n')

        file.read_file()

        file.out_file_write('\n')
