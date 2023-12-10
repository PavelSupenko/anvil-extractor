from abc import ABC


class FileDataBase(ABC):

    def __init__(self):
        self.children: list[FileDataBase] = []
        self.parent: FileDataBase = None

    def add_child(self, child: 'FileDataBase'):
        self.children.append(child)

    def add_parent(self, parent: 'FileDataBase'):
        self.parent = parent

    def get_name_data(self):
        raise NotImplementedError

    def get_type_data(self):
        raise NotImplementedError

    def get_additional_data(self):
        raise NotImplementedError
