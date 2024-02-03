from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import numpy


class Reader(BaseFile):
    ResourceType = 0x0984415E
    VisualType = 0xEC658D29

    def read(self, file_id: int, file: FileDataWrapper):
        # maybe there is no check byte in AC2 ?
        check_byte = file.read_uint_8()  # checkbyte 03 to continue (other stuff to not? have seen 00 with data after)
        # if check_byte == 0:
        #     for _ in range(2):
        #         file.read_file()
        file.out_file_write('Transformation Matrix\n')
        self.transformation_matrix = file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')
        self.nested_files = []

        file.out_file_write('\n')
        # count1 = file.read_uint_32()
        # if count1 > 10000:
        #     raise Exception('error reading entity file')

        # Find visual ID, read it and ignore everything else
        rest_of_file = file.read_rest()
        visual_files_data = self.find_sub_files(rest_of_file, b'\x29\x8D\x65\xEC')

        for visual_file_data in visual_files_data:
            visual_file_wrapper = FileDataWrapper(visual_file_data, file.game_data)
            visual_file = visual_file_wrapper.read_file_data(visual_file_wrapper.file_id, visual_file_wrapper.resource_type)
            self.nested_files.append(visual_file)
