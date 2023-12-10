from model.files.tree.file_data_base import FileDataBase


class SystemFileData(FileDataBase):
    def __init__(self, path: str):
        super().__init__()
        self.path = path

        file_name = path.split('/')[-1].split('.')
        self.name = file_name[0]

        type_from_path = file_name[1] if len(file_name) > 1 else ''
        self.type = type_from_path

    def __str__(self):
        return f"{self.name} - type:{self.type}"

    def get_name_data(self):
        return self.name

    def get_type_data(self):
        return self.type

    def get_additional_data(self):
        return ''
