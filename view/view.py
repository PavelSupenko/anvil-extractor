import logging
import os
from typing import Callable

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QAction

from model.files.tree.file_data import FileData
from view.status_bar import StatusBar
from model.files.tree.files_tree import FileTree
from view.tree_view import TreeView


class View(QtWidgets.QApplication):

    def __init__(self, item_clicked_callback: Callable[[str], None]):
        QtWidgets.QApplication.__init__(self)
        # logging.info('Building GUI Window')

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
        self.horizontal_layout.addWidget(self.search_box, 2)
        self.match_case = QtWidgets.QCheckBox('Match Case')
        self.horizontal_layout.addWidget(self.match_case)
        self.regex = QtWidgets.QCheckBox('Regex')
        self.horizontal_layout.addWidget(self.regex)

        self.search_update = QtCore.QTimer()
        self.search_update.setInterval(150)
        self.search_update.start()

        # file tree view
        self.file_view = TreeView(self.central_widget, self.icons, item_clicked_callback)
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

        self.load_style('QDarkStyle')
        self.translate_()

    def show(self):
        self.main_window.show()

    def wait(self):
        return self.exec()

    def translate_(self):
        self.main_window.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "Anvil extractor"))

    def reset_tree(self, tree: FileTree):
        self.file_view.reset_tree(tree)

    def update_tree(self, parent_name: str, node_data: FileData):
        self.file_view.update_tree(parent_name, node_data)

    def load_style(self, style_name: str):
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
