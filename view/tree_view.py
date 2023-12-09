from typing import Callable

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTreeWidgetItem, QMenu
from PySide6.QtGui import QIcon
from PySide6 import QtWidgets

from model.files.tree.file_data import FileData


class TreeView(QtWidgets.QTreeWidget):

    def __init__(self, parent: QtWidgets.QWidget, icons, handle_item_clicked: Callable[[str], None]):
        QtWidgets.QTreeWidget.__init__(self, parent)
        # self.setHeaderHidden(True)

        self.item_clicked_callback = handle_item_clicked

        self.icons = icons
        self.tree = None

        self.itemDoubleClicked.connect(self.handle_item_double_clicked)

    def reset_tree(self, tree):
        self.tree = tree

        self.clear()
        self.setHeaderLabels(["Name", "File Type"])
        self._set_column_proportions(0.75, 0.25)  # Set proportional column widths
        self._add_nodes_to_tree(self.invisibleRootItem(), [self.tree.root])

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_context_menu_event)

    def update_tree(self, parent_name: str, node_data: FileData):
        parent_item = None
        items = self.findItems(parent_name, Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive)
        for item in items:
            if item.text(0) == parent_name:
                parent_item = item
                break

        if parent_item:
            self._add_node_to_tree(parent_item, node_data)

    def handle_item_double_clicked(self, item: QTreeWidgetItem, column: int):
        item_name: str = item.text(0)
        self.item_clicked_callback(item_name)

    def handle_context_menu_event(self, pos):
        item = self.itemAt(pos)
        if item is not None:
            menu = QMenu(self)
            menu.addAction("Action 1", lambda: self.handle_action(item, "Action 1"))
            menu.addAction("Action 2", lambda: self.handle_action(item, "Action 2"))
            menu.exec_(self.mapToGlobal(pos))

    def handle_action(self, item, action_text):
        print(f"Performing '{action_text}' on item '{item.text(0)}'")

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._set_column_proportions(0.75, 0.25)

    def _set_column_proportions(self, name_proportion, type_proportion):
        total_width = self.width()
        name_width = total_width * name_proportion
        type_width = total_width * type_proportion
        self.setColumnWidth(0, int(name_width))
        self.setColumnWidth(1, int(type_width))

    def _add_nodes_to_tree(self, parent_item, nodes: list[FileData]):
        for node in nodes:
            self._add_node_to_tree(parent_item, node)

    def _add_node_to_tree(self, parent_item, node: FileData):
        file_type = node.type

        item: QTreeWidgetItem

        if file_type in self.icons:
            item = QTreeWidgetItem(parent_item, [node.name, node.type])
            item.setIcon(0, QIcon(self.icons[file_type]))
            item.setText(1, file_type)
        else:
            item = QTreeWidgetItem(parent_item, [node.name, ''])

            if node.depth == 1:
                item.setIcon(0, QIcon(self.icons['directory']))
            else:
                item.setIcon(0, QIcon(self.icons['unknown_file']))

        parent_item.addChild(item)

        if node.children:
            self._add_nodes_to_tree(item, node.children)
