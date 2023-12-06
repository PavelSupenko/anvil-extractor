from typing import Dict, Union, List
from PySide6 import QtWidgets, QtGui, QtCore


class ContextMenu(QtWidgets.QMenu):
    """Context menu for use upon right click of an item in the file tree to access the plugin system."""

    def __init__(self: pyUbiForge, icons: Dict[str, QtGui.QIcon], plugin_names: List[str], file_id: Union[str, int],
                 forge_file_name: Union[None, str], datafile_id: Union[None, int]):
        QtWidgets.QMenu.__init__(self)
        self.icons = icons

        for plugin_name in sorted(plugin_names):
            self.add_command(plugin_name, file_id, forge_file_name, datafile_id)

    def add_command(self, plugin_name: str, file_id: Union[str, int], forge_file_name: Union[None, str] = None,
                    datafile_id: Union[None, int] = None):
        """Workaround for plugin in post method getting overwritten which lead to all options calling the last plugin."""
        if right_click_plugins.get_screen_options(plugin_name, []) is None:
            self.addAction(
                plugin_name,
                lambda: self.run_plugin(plugin_name, file_id, forge_file_name, datafile_id)
            )
        else:
            self.addAction(
                self.icons.get('context_right_click_icon', None),
                plugin_name,
                lambda: self.run_plugin(plugin_name, file_id, forge_file_name, datafile_id)
            )

    def run_plugin(self, plugin_name: str, file_id: Union[str, int], forge_file_name: Union[None, str] = None,
                   datafile_id: Union[None, int] = None) -> None:
        """Method to run and handle plugin options."""
        right_click_plugins.run(plugin_name, file_id, forge_file_name, datafile_id)

    def mousePressEvent(self, event: QtGui.QMouseEvent):
        if event.button() == QtCore.Qt.RightButton:
            entry = self.actionAt(event.pos())
            if entry is not None:
                plugin_name = entry.text()
                options = []
                escape = False
                new_screen = right_click_plugins.get_screen_options(plugin_name, options)
                while new_screen is not None and not escape:
                    # show screen
                    screen = PluginOptionsScreen(plugin_name, new_screen)
                    escape = screen.escape
                    if not escape:
                        # pull options from screen
                        options.append(screen.options)
                        new_screen = right_click_plugins.get_screen_options(plugin_name, options)
                if not escape:
                    entry.trigger()
            else:
                QtWidgets.QMenu.mousePressEvent(self, event)
        elif event.button() == QtCore.Qt.LeftButton:
            QtWidgets.QMenu.mousePressEvent(self, event)
