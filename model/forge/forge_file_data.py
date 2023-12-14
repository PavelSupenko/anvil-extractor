from model.tree import FileDataBase
from model.tree.system_file_data import SystemFileData


class ForgeFileData(FileDataBase):
    def __init__(self, id):
        super().__init__()
        # dictionary key in general, stored for convenience
        self.id = id

        self.name = ''
        self.type = ''

        self.raw_data_offset = ''
        self.raw_data_size = ''

    def add_info(self, type, name):
        self.type = type
        self.name = name

    def add_raw_data(self, raw_data_offset, raw_data_size):
        self.raw_data_offset = raw_data_offset
        self.raw_data_size = raw_data_size

    def get_name_data(self):
        return self.name

    def get_type_data(self):
        return self.type

    def get_additional_data(self):
        return self.id

    def get_parent_forge_file_data(self) -> SystemFileData:
        parent_forge_file_data: SystemFileData = None
        iterative_parent: FileDataBase = self

        while iterative_parent.parent is not None:
            iterative_parent = iterative_parent.parent
            if type(iterative_parent) is SystemFileData:
                parent_forge_file_data = iterative_parent
                break

        return parent_forge_file_data
