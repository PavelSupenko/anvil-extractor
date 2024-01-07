from math import floor
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
        self.sorting_orders = [Qt.AscendingOrder, Qt.AscendingOrder, Qt.AscendingOrder,
                               Qt.AscendingOrder, Qt.AscendingOrder]

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
        self.header().setSectionsClickable(True)
        self.header().sectionClicked.connect(self.sortByColumn)
        self._set_column_proportions(5, 2, 2, 2, 2)  # Set proportional column widths
        self._add_nodes_to_tree(self.invisibleRootItem(), [])

    def sortByColumn(self, logicalIndex):
        current_order = self.sorting_orders[logicalIndex]
        new_order = Qt.DescendingOrder if current_order == Qt.AscendingOrder else Qt.AscendingOrder
        self.sorting_orders = [Qt.AscendingOrder] * self.columnCount()  # Reset all columns to Ascending initially
        self.sorting_orders[logicalIndex] = new_order

        if logicalIndex == 2 or logicalIndex == 3 or logicalIndex == 4:  # Columns where numerical sorting is required
            self.sortByNumericColumn(logicalIndex, new_order)
        else:
            self.sortItems(logicalIndex, new_order)

    def sortByNumericColumn(self, column, order):
        items = [(self.convertToFloat(self.topLevelItem(i).text(column)), self.topLevelItem(i)) for i in range(self.topLevelItemCount())]
        items.sort(key=lambda x: x[0])
        if order == Qt.DescendingOrder:
            items.reverse()
        for i, (_, item) in enumerate(items):
            self.takeTopLevelItem(self.indexOfTopLevelItem(item))
            self.insertTopLevelItem(i, item)

    def convertToFloat(self, text):
        try:
            return float(text)
        except ValueError:
            return 0.0

    def search(self, search_text: str, column: int = 0):
        self.filter_tree_items(search_text.strip(), column)

    def filter_tree_items(self, search_text, column=0):
        self.blockSignals(True)  # Block signals temporarily to avoid triggering events while filtering
        self.filter_children(self.invisibleRootItem(), search_text, column)
        self.blockSignals(False)  # Unblock signals after filtering

    def filter_children(self, item, search_text, column=0) -> bool:
        result: bool = False
        for i in range(item.childCount()):
            child = item.child(i)
            text = child.text(column)  # Assuming a single column tree widget
            satisfy_search = search_text.lower() in text.lower()
            any_child_satisfy_search: bool = self.filter_children(child, search_text, column)

            should_be_shown = satisfy_search or any_child_satisfy_search

            if should_be_shown:
                result = True

            child.setHidden(not should_be_shown)

        return result

    def add_item(self, node_data: FileDataBase):
        parent_data = node_data.parent
        if parent_data is None:
            self._add_node_to_tree(self.invisibleRootItem(), node_data)
            return

        parent_item = self.items_dictionary[parent_data.full_path]
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
        self._set_column_proportions(5, 2, 2, 2, 2)

    def _set_column_proportions(self, name_proportion, type_proportion, id_proportion,
                                position_proportion, size_proportion):

        # 50 is the width of scroll bar
        total_width = self.width() - 50
        total_logical_width = name_proportion + type_proportion + id_proportion + position_proportion + size_proportion

        name_width = total_width * name_proportion / total_logical_width
        type_width = total_width * type_proportion / total_logical_width
        id_width = total_width * id_proportion / total_logical_width
        position_width = total_width * position_proportion / total_logical_width
        size_width = total_width * size_proportion / total_logical_width

        self.setColumnWidth(0, int(floor(name_width)))
        self.setColumnWidth(1, int(floor(type_width)))
        self.setColumnWidth(2, int(floor(id_width)))
        self.setColumnWidth(3, int(floor(position_width)))
        self.setColumnWidth(4, int(floor(size_width)))

    def _add_nodes_to_tree(self, parent_item: TreeViewItem, nodes_data: list[FileDataBase]):
        for node_data in nodes_data:
            self._add_node_to_tree(parent_item, node_data)

    def _add_node_to_tree(self, parent_item: TreeViewItem, node_data: FileDataBase):
        file_type = node_data.type_string

        item: TreeViewItem = TreeViewItem(node_data, parent_item)
        self.items_dictionary[node_data.full_path] = item

        if file_type and file_type in self.icons:
            file_type_icon = QIcon(self.icons[file_type])
            item.set_icon(file_type_icon)
