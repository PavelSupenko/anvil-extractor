from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class FaceInfo(BaseFile):
    ResourceType = 0x325C97EE
    
    def __init__(
        self,
        file_id: int,
        file: FileDataWrapper
    ):
        super().__init__(file_id, file)
        file.read_uint_32()
        file.read_uint_8()
        file.read_uint_8()
        file.read_uint_8()
