import logging
import os
import subprocess
import sys
from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction

from model.export.export_plugin_base import ExportPluginBase
from model.settings.export_settings_loader import ExportSettingsLoader
from model.settings.game_settings_loader import GameSettingsLoader
from model.tree.file_data_base import FileDataBase
from view.context_menu.export_context_menu_factory import ExportContextMenuFactory
from view.export_settings_view import ExportSettingsView
from view.game_settings_view import GameSettingsView
from view.status_bar import StatusBar
from view.tree.tree_view import TreeView
from view.tree.tree_view_item import TreeViewItem


class View(QtWidgets.QApplication):

    def __init__(self,
                 item_clicked_callback: Callable[[FileDataBase], None],
                 plugin_clicked_callback: Callable[[FileDataBase, ExportPluginBase], None],
                 export_context_menu_factory: ExportContextMenuFactory,
                 export_settings_loader: ExportSettingsLoader,
                 game_settings_loader: GameSettingsLoader
                 ):
        QtWidgets.QApplication.__init__(self)

        self.export_settings_loader = export_settings_loader
        self.game_settings_loader = game_settings_loader
        self.export_context_menu_factory = export_context_menu_factory
        self.item_clicked_callback = item_clicked_callback
        self.plugin_clicked_callback = plugin_clicked_callback

        # load the style
        self.icons = {}

        # set up main window
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setObjectName("MainWindow")
        self.main_window.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.main_window.resize(1000, 800)
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.central_widget.setObjectName("centralwidget")
        self.main_window.setCentralWidget(self.central_widget)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName("verticalLayout")
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.vertical_layout.addLayout(self.horizontal_layout)

        # search box
        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setObjectName("search_box")
        self.search_box.textChanged.connect(self._change_search)
        self.horizontal_layout.addWidget(self.search_box, 2)

        # file tree view
        self.file_view = TreeView(self.central_widget, self.icons, self.handle_item_clicked,
                                  self.handle_item_right_clicked)
        self.file_view.setObjectName("file_view")
        self.vertical_layout.addWidget(self.file_view)

        # menu options
        self.menubar = QtWidgets.QMenuBar()
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 26))
        self.menubar.setObjectName("menubar")
        self.main_window.setMenuBar(self.menubar)

        options_menu_item = self.menubar.addMenu('&Options')
        export_options_action = QAction('&Export options', self)
        export_options_action.triggered.connect(lambda: self._show_export_options())
        options_menu_item.addAction(export_options_action)

        game_options_action = QAction('&Game options', self)
        game_options_action.triggered.connect(lambda: self._show_game_options())
        options_menu_item.addAction(game_options_action)

        support_menu_item = self.menubar.addMenu('&Support')
        donate_original_author = QAction('&Donate to original author', self)
        donate_original_author.triggered.connect(lambda: self._donate_to_original_author())
        support_menu_item.addAction(donate_original_author)

        donate_refactoring_author = QAction('&Donate to refactoring author', self)
        donate_refactoring_author.triggered.connect(lambda: self._donate_to_original_author())
        support_menu_item.addAction(donate_refactoring_author)

        # statusbar
        self.statusbar = QtWidgets.QStatusBar()
        self.statusbar.setObjectName("statusbar")
        self.main_window.setStatusBar(self.statusbar)

        status_bar_handler = logging.StreamHandler(
            StatusBar(self, self.statusbar)
        )
        status_bar_handler.setFormatter(
            logging.Formatter('%(message)s')
        )

        logging.getLogger('').addHandler(
            status_bar_handler
        )

        self._load_style('QDarkStyle')
        self.translate_()

    def show(self):
        self.main_window.show()

    def wait(self):
        return self.exec()

    def translate_(self):
        self.main_window.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Anvil extractor"))

    def reset_tree(self):
        self.file_view.reset_tree()

    def add_item(self, node_data: FileDataBase):
        self.file_view.add_item(node_data)

    def handle_item_clicked(self, item: TreeViewItem):
        self.item_clicked_callback(item.file_data)

    def handle_item_right_clicked(self, item: TreeViewItem, parent: TreeView, pos: QPoint):
        context_menu = self.export_context_menu_factory.create(item=item, parent=parent,
                                                               click_callback=self.plugin_clicked_callback)
        context_menu.exec_(parent.mapToGlobal(pos))

    def _change_search(self, text: str):
        self.file_view.search(text)

    def _load_style(self, style_name: str):
        resources_path = os.path.join(os.path.dirname(__file__), 'resources')
        style_path = os.path.join(resources_path, 'themes', style_name, 'style.qss')
        icons_path = os.path.join(resources_path, 'icons')
        style_icons_path = os.path.join(resources_path, 'themes', style_name, 'icons')

        with open(style_path) as style:
            self.setStyleSheet(style.read())

        for icon in os.listdir(icons_path):
            self.icons[os.path.splitext(icon)[0]] = QtGui.QIcon(os.path.join(icons_path, icon))
        if os.path.isdir(style_icons_path):
            for icon in os.listdir(style_icons_path):
                self.icons[os.path.splitext(icon)[0]] = QtGui.QIcon(os.path.join(style_icons_path, icon))

    def _show_export_options(self):
        settings_view = ExportSettingsView(self.export_settings_loader)
        settings_view.exec_()

    def _show_game_options(self):
        settings_view = GameSettingsView(self.game_settings_loader)
        settings_view.exec_()

    @staticmethod
    def _donate_to_original_author():
        if sys.platform == 'win32':
            os.startfile('https://www.paypal.me/gentlegiantJGC')
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', 'https://www.paypal.me/gentlegiantJGC'])
        else:
            try:
                subprocess.Popen(['xdg-open', 'https://www.paypal.me/gentlegiantJGC'])
            except OSError:
                pass
