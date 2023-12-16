from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class MeshData(BaseFile):
    ResourceType = 0x0645ABB5
    
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_uint_8()
        file.read_uint_8()
        file.read_uint_8()
        for _ in range(2):
            count = file.read_uint_32()
            for _ in range(count):
                mesh_primitive = file.read_file()
                assert mesh_primitive.resource_type == 0xA57387EF, "Expected a MeshPrimitive"
        for _ in range(6):
            bcount = file.read_uint_32()
            file.read_bytes(bcount)
