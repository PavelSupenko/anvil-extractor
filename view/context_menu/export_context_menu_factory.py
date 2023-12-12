from typing import Callable

from PySide6.QtWidgets import QMenu

from model.export.export_plugin_base import ExportPluginBase
from model.files.tree.file_data_base import FileDataBase
from view.context_menu.export_context_menu import ExportContextMenu
from view.tree.tree_view import TreeView
from view.tree.tree_view_item import TreeViewItem


class ExportContextMenuFactory:
    def __init__(self, export_plugins: list[ExportPluginBase]):
        self.export_plugins = export_plugins

    def create(self, item: TreeViewItem, parent: TreeView,
               click_callback: Callable[[FileDataBase, ExportPluginBase], None]) -> QMenu:
        menu = ExportContextMenu(parent, item)

        for plugin in self.export_plugins:
            menu.addAction(plugin.plugin_name, lambda plugin_lock=plugin: click_callback(item.file_data, plugin_lock))

        return menu
