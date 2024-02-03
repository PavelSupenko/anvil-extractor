from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import numpy
import logging


class Reader(BaseFile):
    ResourceType = 0x536E963B
    def read(self, file_id: int, file: FileDataWrapper):
        self.mesh_id = None
        self.bounding_box = []
        self.transformation_matrix = []

        temp1 = file.read_bytes(1)
        self.mesh_id = file.read_file_id()

        # Here is the problem that compiled mesh has unstable size and I think transformation matrix in AC2
        # is located not after the compiled mesh and material references
        file.read_bytes(35)  # contains a compiled mesh instance 4368101B

        # file.out_file_write('Transformation Matrix\n')
        # transformation_matrix = file.read_numpy(numpy.float16, 32).reshape((4, 4), order='F')
        # print(f'Transformation matrix: {transformation_matrix}')
        # self.transformation_matrix.append(transformation_matrix)
        # file.read_bytes(3)
        # file.out_file_write('\n')

        count1 = file.read_uint_32()  # number of textures to follow
        file.out_file_write('\n')

        # internal files in ACU is always material references 0x995BFBF5
        internal_files = []
        for n in range(count1):
            internal_file = file.read_file()  # file id always 0x00000000
            internal_files.append(internal_file)

        return

        # file.read_bytes(8) # two counts. first count for transformation matrix. second for more things?
        count2 = file.read_uint_32()
        if count2 > 10000:
            raise Exception(f'count2:{count2} is too large. Aborting')

        for _ in range(count2):
            self.transformation_matrix.append(file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F'))
            file.out_file_write('\n')

        count3 = file.read_uint_32()
        if count3 > 10000:
            raise Exception('count3 is too large. Aborting')

        for _ in range(count3):
            sub_file_container = file.read_file()
            if sub_file_container.resource_type == '4AEC3476':
                self.bounding_box.append(sub_file_container.bounding_box)
        file.out_file_write('\n')
