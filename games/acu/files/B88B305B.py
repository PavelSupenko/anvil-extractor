from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
import logging


class Reader(BaseFile):
    ResourceType = 0xB88B305B
    def read(self, file_id: int, file: FileDataWrapper):
        check = file.read_uint_8()
        if check == 1:
            file.read_bytes(1)
            file.read_file_id()
        elif check == 3:
            file.read_bytes(9)
        else:
            logging.warning(f'Expected check to be 1 or 3 but got {check}')
            raise Exception

        file.read_bytes(1)

        check = file.read_uint_8()
        if check == 1:
            file.read_bytes(1)
            file.read_file_id()
        elif check == 3:
            file.read_bytes(9)
        else:
            logging.warning(f'Expected check to be 1 or 3 but got {check}')
            raise Exception
