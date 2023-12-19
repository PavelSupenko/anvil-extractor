import logging
import os
from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtCore import QPoint
from PySide6.QtGui import QAction

from model.export.export_plugin_base import ExportPluginBase
from model.tree.file_data_base import FileDataBase
from view.context_menu.export_context_menu_factory import ExportContextMenuFactory
from view.status_bar import StatusBar
from view.tree.tree_view import TreeView
from view.tree.tree_view_item import TreeViewItem


class View(QtWidgets.QApplication):

    def __init__(self,
                 item_clicked_callback: Callable[[FileDataBase], None],
                 plugin_clicked_callback: Callable[[FileDataBase, ExportPluginBase], None],
                 export_context_menu_factory: ExportContextMenuFactory,
                 ):
        QtWidgets.QApplication.__init__(self)

        self.export_context_menu_factory = export_context_menu_factory
        self.item_clicked_callback = item_clicked_callback
        self.plugin_clicked_callback = plugin_clicked_callback

        # load the style
        self.icons = {}

        # set up main window
        self.main_window = QtWidgets.QMainWindow()
        self.main_window.setObjectName("MainWindow")
        self.main_window.setWindowIcon(QtGui.QIcon('icon.ico'))
        self.main_window.resize(809, 698)
        self.central_widget = QtWidgets.QWidget(self.main_window)
        self.central_widget.setObjectName("centralwidget")
        self.main_window.setCentralWidget(self.central_widget)
        self.vertical_layout = QtWidgets.QVBoxLayout(self.central_widget)
        self.vertical_layout.setObjectName("verticalLayout")
        self.horizontal_layout = QtWidgets.QHBoxLayout()
        self.horizontal_layout.setObjectName("horizontal_layout")
        self.vertical_layout.addLayout(self.horizontal_layout)

        # drop down box to select the game
        self.game_select = QtWidgets.QComboBox()
        self.game_select.setObjectName("game_select")
        self.game_select.addItems(['ACU', 'AC1', 'AC2'])
        self.horizontal_layout.addWidget(self.game_select, 1)

        # search box
        self.search_box = QtWidgets.QLineEdit()
        self.search_box.setClearButtonEnabled(True)
        self.search_box.setObjectName("search_box")
        self.search_box.textChanged.connect(self._change_search)
        self.horizontal_layout.addWidget(self.search_box, 2)
        # self.match_case = QtWidgets.QCheckBox('Match Case')
        # self.horizontal_layout.addWidget(self.match_case)
        # self.regex = QtWidgets.QCheckBox('Regex')
        # self.horizontal_layout.addWidget(self.regex)

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

        games_menu_item = self.menubar.addMenu('&Games')
        games_action = QAction('&Games settings', self)
        # games_action.triggered.connect(lambda: self._show_games())
        games_menu_item.addAction(games_action)

        options_menu_item = self.menubar.addMenu('&Options')
        options_action = QAction('&General options', self)
        # options_action.triggered.connect(lambda: self._show_options())
        options_menu_item.addAction(options_action)

        support_menu_item = self.menubar.addMenu('&Support')
        support_action = QAction('&Donate', self)
        # support_action.triggered.connect(lambda: self._donate())
        support_menu_item.addAction(support_action)

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

    def add_item(self, parent_data: FileDataBase, node_data: FileDataBase):
        self.file_view.add_item(parent_data, node_data)

    def add_items(self, parent_data: FileDataBase, nodes_data: list[FileDataBase]):
        self.file_view.add_items(parent_data, nodes_data)

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
