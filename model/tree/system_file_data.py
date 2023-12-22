import os

from model.tree.file_data_base import FileDataBase


class SystemFileData(FileDataBase):
    def __init__(self, path: str):
        self.path = path

        file_name = path.split('/')[-1].split('.')
        type_from_path = file_name[1] if len(file_name) > 1 else ''

        super().__init__(name=file_name[0], type=type_from_path)

        stat = os.stat(path)
        self.size_mb = round(stat.st_size / 1024 / 1024, 1)

    def __str__(self):
        return f"{self.name} - type:{self.type}"

    @property
    def properties(self) -> list[str]:
        return [self.name, self.type, '', '', self.size_mb]
