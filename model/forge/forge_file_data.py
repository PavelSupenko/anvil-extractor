from model.files.tree.file_data_base import FileDataBase


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
