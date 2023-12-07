from PySide6.QtWidgets import QTreeWidgetItem
from PySide6 import QtWidgets

from model.files.files_tree import FileTree


class TreeView(QtWidgets.QTreeWidget):

    def __init__(self, parent: QtWidgets.QWidget, icons):
        QtWidgets.QTreeWidget.__init__(self, parent)
        self.tree = None

    def set_tree(self, tree):
        self.tree = tree
        self._populate_tree()

    def _populate_tree(self):
        self.clear()
        self._add_to_tree(self.invisibleRootItem(), [self.tree.root])

    def _add_to_tree(self, parent_item, nodes):
        for node in nodes:
            item = QTreeWidgetItem(parent_item, [node.name])
            parent_item.addChild(item)
            if node.children:
                self._add_to_tree(item, node.children)
