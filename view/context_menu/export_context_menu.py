from typing import Callable

from PySide6.QtWidgets import QMenu, QTreeWidget

from model.files.tree.file_data_base import FileDataBase
from view.tree.tree_view_item import TreeViewItem


class ExportContextMenu(QMenu):

    def __init__(self, parent: QTreeWidget, item: TreeViewItem):
        super().__init__(parent)
        self.item = item

    def add_action(self, action_text: str, callback: Callable[[FileDataBase], None]):
        self.addAction(action_text, lambda: callback(self.item.file_data))
