from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import logging


class Reader(BaseFile):
    ResourceType = 0x3BBECB2B
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(11)
        count1 = file.read_uint_32()
        for _ in range(count1):
            file.read_file()

        # 1.1 in float
        # 4 bytes
        # count
        # 00
        # fileID
        # 1.5 in float

        # 2.1 in float
        # count?
        # 00
        # fileID
        # 4 bytes
        # 3 in float
        # count
        # 00
        # fileID
        # count
        # 00
        # fileID

        file.read_bytes(4)  # float
        for _ in range(2):
            count2 = file.read_uint_32()
            if count2 > 10000:
                logging.warning('error reading entity file')
                # convert to an actual logger
                raise Exception()
            for _ in range(count2):
                file.read_bytes(1)
                file.read_file_id()
        file.out_file_write('\n')
