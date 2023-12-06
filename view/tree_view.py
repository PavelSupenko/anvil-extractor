from typing import Dict, Union, Tuple, List, Optional
from PySide6 import QtWidgets, QtGui, QtCore


class TreeView(QtWidgets.QTreeWidget):

    def __init__(self, parent: QtWidgets.QWidget, icons: Dict[str, QtGui.QIcon]):
        QtWidgets.QTreeWidget.__init__(self, parent)
        self.icons = icons
        self._entries: Dict[Tuple[Union[None, str], Union[None, int], Union[None, int]], TreeViewEntry] = {}
        self._search: Dict[str, List[TreeViewEntry]] = {}
        self._game_identifier = None
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_context_menu)

    def load_game(self, game_identifier: str):
        self._entries.clear()
        self._search.clear()
        self.clear()
        self._game_identifier = game_identifier
        self.insert(game_identifier, icon=self.icons['directory'])

    def search(self, search_string: str, match_case: bool, regex: bool) -> None:
        if search_string == '':
            for entry in self._entries.values():
                entry.setHidden(False)
                entry.children_shown = True
        else:
            for entry in self._entries.values():
                entry.setHidden(True)
                entry.children_shown = False
            if regex:
                regex_search = re.compile(search_string)

            for entry_name in self._search.keys():
                if (regex and regex_search.search(entry_name)) \
                        or (
                        not regex and (
                        (match_case and search_string in entry_name)
                        or
                        (not match_case and search_string.lower() in entry_name.lower())
                )
                ):
                    for entry in self._search[entry_name]:
                        entry.recursively_unhide_children()
                        entry.recursively_unhide_parents()

    def insert(self, entry_name: str, forge_file_name: Optional[str] = None, datafile_id: Optional[int] = None,
               file_id: Optional[int] = None, icon: QtGui.QIcon = None) -> None:
        if forge_file_name is not None:
            if datafile_id is not None:
                if file_id is not None:  # the fact that the ends of these align makes me very happy
                    parent = self._entries[(forge_file_name, datafile_id, None)]
                else:
                    parent = self._entries[(forge_file_name, None, None)]
            else:
                parent = self._entries[(None, None, None)]
            entry = TreeViewEntry(parent, entry_name, forge_file_name, datafile_id, file_id, icon=icon)
            parent.addChild(entry)
        else:
            entry = TreeViewEntry(self, entry_name, icon=icon)

        self._entries[(forge_file_name, datafile_id, file_id)] = entry
        if entry.entry_name not in self._search:
            self._search[entry.entry_name] = []
        self._search[entry.entry_name].append(entry)

    def populate_tree(self):
        """A helper function to populate files in the file view."""
        for forge_file_name, forge_file in pyUbiForge.forge_files.items():
            for datafile_id in forge_file.new_datafiles:
                for file_id, file_name in sorted(forge_file.datafiles[datafile_id].files.items(),
                                                 key=lambda v: v[1].lower()):
                    self.insert(
                        file_name,
                        forge_file_name,
                        datafile_id,
                        file_id,
                        icon=self.icons.get(
                            pyUbiForge.temp_files(file_id, forge_file_name, datafile_id).file_type,
                            None
                        )
                    )
            forge_file.new_datafiles.clear()

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        entry: TreeViewEntry = self.itemAt(event.pos())
        if entry is not None and entry.depth == 3 and entry.childCount() == 0:
            forge_file_name, datafile_id = entry.forge_file_name, entry.datafile_id
            pyUbiForge.forge_files[forge_file_name].decompress_datafile(datafile_id)
            self.populate_tree()
        QtWidgets.QTreeWidget.mousePressEvent(self, event)

    def open_context_menu(self, position: QtCore.QPoint):
        entry: TreeViewEntry = self.itemAt(position)
        if entry is not None:
            unique_identifier = (None, entry.forge_file_name, entry.datafile_id, entry.file_id)[entry.depth - 1]
            plugin_names, file_id = right_click_plugins.query(entry.depth, unique_identifier, entry.forge_file_name,
                                                              entry.datafile_id)
            if len(plugin_names) > 0:
                menu = ContextMenu(self.icons, plugin_names, file_id, entry.forge_file_name, entry.datafile_id)
                menu.exec(self.viewport().mapToGlobal(position))
            self.populate_tree()
