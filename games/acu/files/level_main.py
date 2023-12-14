from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from pyUbiForge2.games.ACU import register_file_reader


@register_file_reader('FBB63E47')
class Reader(BaseFile):
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id)
        for _ in range(2):
            file.read_file()  # 7DB083ED  contains data block ids

        file.read_bytes(2)
        self.fakes = file.read_file_id()

        file.read_bytes(2)
        file.read_file_id()

        # sequence data table
        count = file.read_uint_32()
        with file.indent:
            for _ in range(count):
                file.read_bytes(2)
                file.read_file_id()

        file.read_bytes(2)
        file.read_file()

        assert file.read_uint_8() == 0, "check byte failed"
        file.read_file()
