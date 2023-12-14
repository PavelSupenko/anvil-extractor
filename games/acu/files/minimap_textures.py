from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('EE568905')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):

        BaseFile.__init__(self, file_id)
        count1 = file.read_uint_32()
        self.width = self.height = int(count1 ** 0.5)
        self.image_ids = []
        for n in range(count1):
            file.indent()
            file.read_bytes(1)
            self.image_ids.append(file.read_file_id())
            file.indent(-1)
