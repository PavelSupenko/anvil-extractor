from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import logging


class Reader(BaseFile):
    ResourceType = 0x1C4B22AA
    def read(self, file_id: int, file: FileDataWrapper):
        file.read_bytes(5)  # zeros
    # count = file.read_uint_8()
    # if count > 0:
    # 	file.read_bytes(3)
    # 	for _ in range(count):
    # 		file.read_file()
    # 	file.read_bytes(4)
    #
    # b = file.read_uint_8()
    # if b == 3:
    # 	file.read_bytes(9)
    # 	file.read_bytes(4 * file.read_uint_32())
    # elif b == 5:
    # 	file.read_file_id()
    # 	file.read_bytes(5)
    # 	file.read_file_id()
    # else:
    # 	logging.warning('value is not 3 or 5 I don\'t know how to deal with this')
