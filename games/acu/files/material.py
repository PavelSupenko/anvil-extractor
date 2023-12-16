from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x85C817C3
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(2)
        file.read_file_id()
        file.read_bytes(2)
        self.material_set = file.read_file_id()
    
    # file.read_file()
    # file.read_file_id()
