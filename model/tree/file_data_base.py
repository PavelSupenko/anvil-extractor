from abc import ABC
from typing import Union


class FileDataBase(ABC):

    def __init__(self, name: str, type: Union[str, int]):
        self.name = name
        self.type = type

        self.children: list[FileDataBase] = []
        self.parent: FileDataBase = None

        self._full_path = name

    def add_child(self, child: 'FileDataBase'):
        self.children.append(child)

    def add_parent(self, parent: 'FileDataBase'):
        self.parent = parent
        self._full_path = self.recalculate_full_path()

    @property
    def full_path(self) -> str:
        return self._full_path

    def recalculate_full_path(self) -> str:
        string_properties = ''

        for i in range(len(self.properties)):
            if i == 0:
                string_properties += f'{self.properties[i]}'
            else:
                string_properties += f':{self.properties[i]}'

        if self.parent is None:
            return string_properties

        return f'{self.parent.full_path}/{string_properties}'

    @property
    def properties(self) -> list[str]:
        raise NotImplementedError
