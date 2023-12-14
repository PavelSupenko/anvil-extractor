from typing import ForwardRef

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QTreeWidgetItem

from model.tree import FileDataBase


class TreeViewItem(QTreeWidgetItem):
    def __init__(self, file_data: FileDataBase, parent_item: ForwardRef('TreeViewItem') = None):
        super().__init__(parent_item, [file_data.get_name_data(), file_data.get_type_data(), file_data.get_additional_data()])

        # main data
        self.file_data = file_data

        # tree data

        if type(parent_item) is FileDataBase:
            self.depth = parent_item.depth + 1
        else:
            self.depth = 1

        self.parent: TreeViewItem = parent_item
        self.children: list[TreeViewItem] = []

        self.parent.addChild(self)
        self.update()

    def update(self):
        self.setText(0, str(self.file_data.get_name_data()))
        self.setText(1, str(self.file_data.get_type_data()))
        self.setText(2, str(self.file_data.get_additional_data()))

    def set_icon(self, icon: QIcon):
        self.setIcon(0, icon)
