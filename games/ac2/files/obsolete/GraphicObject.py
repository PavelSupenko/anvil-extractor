from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class GraphicObject(BaseFile):
    ResourceType = 0xEC6AC357

    def read(self, file_id: int, file: FileDataWrapper):
        file.read_int_32()
        file.read_int_8()
