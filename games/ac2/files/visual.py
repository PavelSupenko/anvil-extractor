from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xEC658D29
    MeshInstanceDataType = 0x536E963B

    def read(self, file_id: int, file: FileDataWrapper):
        self.nested_files = {}

        temp1 = file.read_bytes(3)
        temp2 = file.read_file_id()
        temp3 = file.read_bytes(1)

        # Find mesh instance data ID, read it and ignore everything else
        rest_of_file = file.read_rest()
        mesh_instance_files_data = self.find_sub_files(rest_of_file, b'\x3B\x96\x6E\x53')

        for mesh_instance_file_data in mesh_instance_files_data:
            mesh_instance_file_wrapper = FileDataWrapper(mesh_instance_file_data, file.game_data)
            mesh_instance_file = mesh_instance_file_wrapper.read_file_data(mesh_instance_file_wrapper.file_id, mesh_instance_file_wrapper.resource_type)
            self.nested_files[mesh_instance_file_wrapper.resource_type] = mesh_instance_file

        # nested_file = file.read_file()
        # self.nested_files[nested_file.resource_type] = nested_file
        # file.read_bytes(1)

        file.out_file_write('\n')

        # for _ in range(7):
        #     file.read_float_32()
