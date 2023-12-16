from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x9EF59664
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(13)
