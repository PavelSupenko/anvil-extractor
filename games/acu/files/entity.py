from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import numpy


class Reader(BaseFile):
    ResourceType = 0x0984415E

    def read(self, file_id: int, file: FileDataWrapper):
        check_byte = file.read_uint_8()  # checkbyte 03 to continue (other stuff to not? have seen 00 with data after)
        if check_byte == 0:
            for _ in range(2):
                file.read_file()
        file.out_file_write('Transformation Matrix\n')
        self.transformation_matrix = file.read_numpy(numpy.float32, 64).reshape((4, 4), order='F')

        file.out_file_write('\n')
        count1 = file.read_uint_32()
        if count1 > 10000:
            raise Exception('error reading entity file')

        self.nested_files = []

        for _ in range(count1):
            file.out_file_write('\n')
            with file.indent:
                file.read_bytes(2)  # usually in [b'\x04\x00', b'\x00\x01'] but not always
                self.nested_files.append(file.read_file())

        # float * 7

        # 37 bytes
        # 2 bytes
        # float

        # bouding box
        # id
        # type
        # float32 * 6
        # int32

        # entity descriptor
        # 19 bytes

        file.out_file_write('\n')

        file.read_bytes(43)

        # data layer filter
        # 4 count, more data in here sometimes
        for _ in range(3):
            file.read_file()

        # 03 end file?
        check_byte_2 = file.read_uint_8()
        if check_byte_2 == 0:
            file.read_file()
        elif check_byte_2 != 3:
            raise Exception
        file.out_file_write('\n')
