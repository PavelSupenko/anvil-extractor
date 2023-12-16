from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class MeshPrimitive(BaseFile):
    ResourceType = 0xA57387EF
    
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_uint_32()
        file.read_uint_32()
        file.read_uint_32()
        file.read_uint_32()
        file.read_uint_32()
        file.read_uint_32()
