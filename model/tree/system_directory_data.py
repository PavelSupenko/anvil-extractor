from model.tree.file_data_base import FileDataBase


class SystemDirectoryData(FileDataBase):
    def __init__(self, path: str):
        super().__init__(name=path.split('/')[-1], type='directory')
        self.path = path

    def __str__(self):
        return f"{self.name} - path:{self.path}"

    @property
    def properties(self) -> list[str]:
        return [self.name, self.type, '', self.path, '']
