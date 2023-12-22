from typing import Callable

from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QIcon
from PySide6 import QtWidgets

from model.tree.file_data_base import FileDataBase
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

        self.items_dictionary = {}

        self.item_clicked_callback = handle_item_clicked
        self.item_right_clicked_callback = handle_item_right_click
        self.icons = icons

        self.itemClicked.connect(self.handle_item_clicked)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.handle_context_menu_event)

    def reset_tree(self):
        self.items_dictionary = {}
        self.clear()
        self.setHeaderLabels(["Name", "File Type", "File ID", "Position", "Size"])
        self._set_column_proportions(0.3, 0.2, 0.2, 0.15, 0.15)  # Set proportional column widths
        self._add_nodes_to_tree(self.invisibleRootItem(), [])

    def update_visual_tree(self):
        pass

    def search(self, search_text: str):
        self.filter_tree_items(search_text.strip())

    def filter_tree_items(self, search_text):
        self.blockSignals(True)  # Block signals temporarily to avoid triggering events while filtering
        self.filter_children(self.invisibleRootItem(), search_text)
        self.blockSignals(False)  # Unblock signals after filtering

    def filter_children(self, item, search_text) -> bool:
        result: bool = False
        for i in range(item.childCount()):
            child = item.child(i)
            text = child.text(0)  # Assuming a single column tree widget
            satisfy_search = search_text.lower() in text.lower()
            any_child_satisfy_search: bool = self.filter_children(child, search_text)

            should_be_shown = satisfy_search or any_child_satisfy_search

            if should_be_shown:
                result = True

            child.setHidden(not should_be_shown)

        return result

    def add_item(self, parent_data: FileDataBase, node_data: FileDataBase):
        if parent_data is None:
            self._add_node_to_tree(self.invisibleRootItem(), node_data)
            return

        parent_item = self.items_dictionary[parent_data.full_path]
        self._add_node_to_tree(parent_item, node_data)

    def add_items(self, parent_data: FileDataBase, nodes_data: list[FileDataBase]):
        for node_data in nodes_data:
            self.add_item(parent_data, node_data)

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
        self._set_column_proportions(0.3, 0.2, 0.2, 0.15, 0.15)

    def _set_column_proportions(self, name_proportion, type_proportion, id_proportion,
                                position_proportion, size_proportion):
        total_width = self.width()
        name_width = total_width * name_proportion
        type_width = total_width * type_proportion
        id_width = total_width * id_proportion
        position_width = total_width * position_proportion
        size_width = total_width * size_proportion
        self.setColumnWidth(0, int(name_width))
        self.setColumnWidth(1, int(type_width))
        self.setColumnWidth(2, int(id_width))
        self.setColumnWidth(3, int(position_width))
        self.setColumnWidth(4, int(size_width))

    def _add_nodes_to_tree(self, parent_item: TreeViewItem, nodes_data: list[FileDataBase]):
        for node_data in nodes_data:
            self._add_node_to_tree(parent_item, node_data)

    def _add_node_to_tree(self, parent_item: TreeViewItem, node_data: FileDataBase):
        file_type = node_data.type

        item: TreeViewItem = TreeViewItem(node_data, parent_item)
        self.items_dictionary[node_data.full_path] = item

        if file_type and file_type in self.icons:
            file_type_icon = QIcon(self.icons[file_type])
            item.set_icon(file_type_icon)
