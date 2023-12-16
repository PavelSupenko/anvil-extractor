from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class PackedOrthonormalMatrix(BaseFile):
    ResourceType = 0x05358B33
    
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_uint_16()
        file.read_uint_16()
        file.read_uint_16()
        file.read_uint_16()
        file.read_uint_16()
        file.read_uint_16()
        file.read_uint_32()
        file.read_uint_32()
