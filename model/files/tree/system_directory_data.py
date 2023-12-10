from model.files.tree.file_data_base import FileDataBase


class SystemDirectoryData(FileDataBase):
    def __init__(self, path: str):
        super().__init__()
        self.path = path
        self.name = path.split('/')[-1]

    def __str__(self):
        return f"{self.name} - path:{self.path}"

    def get_name_data(self):
        return self.name

    def get_type_data(self):
        return 'directory'

    def get_additional_data(self):
        return ''
