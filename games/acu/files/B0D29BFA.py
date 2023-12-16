from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xB0D29BFA
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_struct('37f')
        file.read_struct('16f')
