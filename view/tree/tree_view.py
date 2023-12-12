from typing import Callable

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon
from PySide6 import QtWidgets

from model.files.tree.file_data_base import FileDataBase
from view.tree.tree_view_item import TreeViewItem


class TreeView(QtWidgets.QTreeWidget):

    def __init__(self,
                 parent: QtWidgets.QWidget,
                 icons,
                 handle_item_clicked: Callable[[TreeViewItem], None],
                 handle_item_right_click: Callable[[TreeViewItem, 'TreeView', QPoint], None],
                 ):
        QtWidgets.QTreeWidget.__init__(self, parent)
        # self.setHeaderHidden(True)

        self.item_clicked_callback = handle_item_clicked
        self.item_right_clicked_callback = handle_item_right_click
        self.icons = icons

        self.itemClicked.connect(self.handle_item_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_context_menu_event)

    def reset_tree(self):
        self.clear()
        self.setHeaderLabels(["Name", "File Type", "File ID"])
        self._set_column_proportions(0.5, 0.25, 0.25)  # Set proportional column widths
        self._add_nodes_to_tree(self.invisibleRootItem(), [])

    def update_visual_tree(self):
        pass

    def update_tree(self, parent_data: FileDataBase, node_data: FileDataBase):
        if parent_data is None:
            self._add_node_to_tree(self.invisibleRootItem(), node_data)
            return

        parent_item = None
        items = self.findItems(parent_data.get_name_data(), Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive)
        for item in items:
            if item.text(0) == parent_data.get_name_data():
                parent_item = item
                break

        self._add_node_to_tree(parent_item, node_data)

    def update_tree_by_name(self, parent_name: str, node_data: FileDataBase):
        if parent_name == '':
            self._add_node_to_tree(self.invisibleRootItem(), node_data)
            return

        parent_item = None
        items = self.findItems(parent_name, Qt.MatchFlag.MatchExactly | Qt.MatchFlag.MatchRecursive)
        for item in items:
            if item.text(0) == parent_name:
                parent_item = item
                break

        if parent_item:
            self._add_node_to_tree(parent_item, node_data)

    def handle_item_clicked(self, item: TreeViewItem, column: int):
        self.item_clicked_callback(item)

    def handle_context_menu_event(self, pos: QPoint):
        item = self.itemAt(pos)
        if item is None or type(item) is not TreeViewItem:
            print('No tree item at position')
            return

        tree_view_item: TreeViewItem = item
        self.item_right_clicked_callback(tree_view_item, self, pos)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._set_column_proportions(0.5, 0.25, 0.25)

    def _set_column_proportions(self, name_proportion, type_proportion, id_proportion):
        total_width = self.width()
        name_width = total_width * name_proportion
        type_width = total_width * type_proportion
        id_width = total_width * id_proportion
        self.setColumnWidth(0, int(name_width))
        self.setColumnWidth(1, int(type_width))
        self.setColumnWidth(2, int(id_width))

    def _add_nodes_to_tree(self, parent_item: TreeViewItem, nodes_data: list[FileDataBase]):
        for node_data in nodes_data:
            self._add_node_to_tree(parent_item, node_data)

    def _add_node_to_tree(self, parent_item: TreeViewItem, node_data: FileDataBase):
        file_type = node_data.get_type_data()

        item: TreeViewItem = TreeViewItem(node_data, parent_item)

        if file_type and file_type in self.icons:
            file_type_icon = QIcon(self.icons[file_type])
            item.set_icon(file_type_icon)
