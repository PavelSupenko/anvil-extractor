from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0x21795599
    def read(self, file_id: int, file: FileDataWrapper):
        for length in [2, 2, 1, 1, 4, 2, 2]:
            total_count = file.read_uint_32()
            file.indent()
            file.read_bytes(total_count * length)
            file.indent(-1)
        found_count = 0
        empty_count = 0
        filled_count = 0
        # probably not right but this seems to work
        while found_count < total_count or empty_count != filled_count + 1:
            check_byte = file.read_uint_8()
            if check_byte == 0:
                sub_file_container = file.read_file()
                found_count += sub_file_container.count
                if sub_file_container.count > 0:
                    filled_count += 1
                else:
                    empty_count += 1

            elif check_byte == 3:
                filled_count += 1
                continue
            else:
                raise Exception(f'{__name__}: check_byte is not in 0, 3. Exited at count {found_count}/{empty_count}')
        file.read_bytes(8)
        count = file.read_uint_32()
        for _ in range(count):
            check_byte = file.read_bytes(1)
            file.read_file()
        count = file.read_uint_32()
        for _ in range(count):
            file.read_bytes(4)
        file.read_bytes(1)
        for _ in range(7):
            file.read_bytes(4)
        file.read_file()
