from typing import Union, List
from PySide6 import QtWidgets, QtGui


class TreeViewEntry(QtWidgets.QTreeWidgetItem):
    def __init__(self, tree_view: Union[TreeView, 'TreeViewEntry'], entry_name: str, forge_file_name: str = None,
                 datafile_id: int = None, file_id: int = None, icon: QtGui.QIcon = None):
        if file_id is not None:
            public_name = f"{entry_name}\t\t{file_id:016X}"
        elif datafile_id is not None:
            public_name = f"{entry_name}\t\t{datafile_id:016X}"
        else:
            public_name = entry_name
        super().__init__(tree_view, [public_name])
        if icon is not None:
            self.setIcon(0, icon)
        self._entry_name = public_name
        self._forge_file_name = forge_file_name
        self._datafile_id = datafile_id
        self._file_id = file_id
        self._dev_search = None
        self._depth = None
        self.children_shown = True

    @property
    def entry_name(self) -> str:
        return self._entry_name

    @property
    def forge_file_name(self) -> Union[str, None]:
        return self._forge_file_name

    @property
    def datafile_id(self) -> Union[int, None]:
        return self._datafile_id

    @property
    def file_id(self) -> Union[int, None]:
        return self._file_id

    @property
    def dev_search(self) -> List[str]:
        if self._dev_search is None:
            self._dev_search = [f'{attr:016X}' for attr in [self.datafile_id, self.file_id] if attr is not None]
            self._dev_search += [''.join(attr[n:n + 2] for n in reversed(range(0, 16, 2))) for attr in self._dev_search]
        return self._dev_search

    @property
    def depth(self) -> int:
        if self._depth is None:
            if self.forge_file_name is not None:
                if self.datafile_id is not None:
                    if self.file_id is not None:
                        self._depth = 4
                    else:
                        self._depth = 3
                else:
                    self._depth = 2
            else:
                self._depth = 1
        return self._depth

    def search(self, search_string: str) -> bool:
        if search_string == '' or any(
                search_string in attr for attr in [self._entry_name, self._forge_file_name] if attr is not None):
            # if the string is empty or matches one of the parameters unhide self and children.
            self.recursively_unhide_children()
            return True
        elif pyUbiForge.CONFIG.get('dev', False) and any(search_string.upper() in attr for attr in self.dev_search):
            # if in dev mode and matches one of the file ids unhide self and children
            self.recursively_unhide_children()
            return True
        else:
            shown = any([self.child(index).search(search_string) for index in range(self.childCount())])
            self.setHidden(not shown)
            return shown

    def recursively_unhide_children(self):
        if not self.children_shown:
            self.children_shown = True
            self.setHidden(False)
            for index in range(self.childCount()):
                self.child(index).recursively_unhide_children()

    def recursively_unhide_parents(self):
        parent = self.parent()
        if parent is not None:
            parent.setHidden(False)
            parent.recursively_unhide_parents()
