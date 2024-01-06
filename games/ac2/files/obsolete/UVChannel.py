from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class UVChannel(BaseFile):
    ResourceType = 0xBDAD8273
    
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_uint_32()
        file.read_uint_8()
        bcount = file.read_uint_32()
        file.read_bytes(bcount*4*2)
        bcount = file.read_uint_32()
        file.read_bytes(bcount*4*1)
