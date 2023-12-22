from model.tree.file_data_base import FileDataBase
from model.tree.system_file_data import SystemFileData


class ForgeFileData(FileDataBase):
    def __init__(self, id):
        super().__init__(name='', type='')
        self.id = id

    def add_info(self, type, name):
        self.type = type
        self.name = name

    @property
    def properties(self) -> list[str]:
        return [self.name, self.type, self.id]
        # return [self.name, f'{self.type:016X}', self.id]

    def get_top_parent_forge_item_file_data(self) -> 'ForgeFileData':
        iterative_parent: FileDataBase = self

        while type(iterative_parent.parent) is not SystemFileData:
            iterative_parent = iterative_parent.parent

        return iterative_parent

    def get_parent_forge_file_data(self) -> SystemFileData:
        parent_forge_file_data: SystemFileData = None
        iterative_parent: FileDataBase = self

        while iterative_parent.parent is not None:
            iterative_parent = iterative_parent.parent
            if type(iterative_parent) is SystemFileData:
                parent_forge_file_data = iterative_parent
                break

        return parent_forge_file_data
