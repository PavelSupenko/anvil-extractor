from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class MeshInstancingData(BaseFile):
    ResourceType = 0xB1D34C1
    
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_uint_8()
        file.read_uint_8()
        file.read_uint_8()
        file.read_uint_8()
        file.read_uint_16()
        file.read_file_switch()
        for _ in range(0x2A):
            file.read_uint_8()
