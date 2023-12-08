from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTreeWidgetItem
from PySide6 import QtWidgets

from model.files.file_data import FileData


class TreeView(QtWidgets.QTreeWidget):

    def __init__(self, parent: QtWidgets.QWidget, icons):
        QtWidgets.QTreeWidget.__init__(self, parent)
        self.icons = icons
        self.tree = None

        self.itemDoubleClicked.connect(self.handle_item_double_clicked)

    def set_tree(self, tree):
        self.tree = tree
        self._populate_tree()

    @staticmethod
    def handle_item_double_clicked(item: QTreeWidgetItem, column: int):
        print(f'Item {item.text(column)} double clicked')

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._set_column_proportions(0.75, 0.25)

    def _populate_tree(self):
        self.clear()
        self.setHeaderLabels(["Name", "File Type"])
        self._set_column_proportions(0.75, 0.25)  # Set proportional column widths
        self._add_to_tree(self.invisibleRootItem(), [self.tree.root])

    def _set_column_proportions(self, name_proportion, type_proportion):
        total_width = self.width()
        name_width = total_width * name_proportion
        type_width = total_width * type_proportion
        self.setColumnWidth(0, int(name_width))
        self.setColumnWidth(1, int(type_width))

    def _add_to_tree(self, parent_item, nodes: list[FileData]):
        for node in nodes:
            file_type = node.type

            item: QTreeWidgetItem

            if file_type in self.icons:
                item = QTreeWidgetItem(parent_item, [node.name, node.type])
                item.setIcon(0, QIcon(self.icons[file_type]))
                item.setText(1, file_type)
            else:
                item = QTreeWidgetItem(parent_item, [node.name, '_'])

            parent_item.addChild(item)
            if node.children:
                if not file_type:
                    item.setIcon(0, QIcon(self.icons['directory']))

                self._add_to_tree(item, node.children)
