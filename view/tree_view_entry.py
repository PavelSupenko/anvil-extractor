from typing import Union, List
from PySide6 import QtWidgets, QtGui

from view.tree_view import TreeView


class TreeViewEntry(QtWidgets.QTreeWidgetItem):
    def __init__(self):
        super().__init__()