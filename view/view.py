import logging
import os

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QAction

from status_bar import StatusBar
from tree_view import TreeView


class View(QtWidgets.QApplication):

    def __init__(self):
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
        self.game_select.addItems(['ACU','AC1','AC2'])
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
        self.file_view = TreeView(self.central_widget, self.icons)
        self.file_view.setObjectName("file_view")
        self.file_view.setHeaderHidden(True)
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

        self.main_window.show()
        self.exec()

    def translate_(self):
        self.main_window.setWindowTitle(QtWidgets.QApplication.translate("MainWindow", "ACExplorer"))

    def load_style(self, style_name: str):
        with open(f'./resources/themes/{style_name}/style.qss') as style:
            self.setStyleSheet(style.read())
        for icon in os.listdir('resources/icons'):
            self.icons[os.path.splitext(icon)[0]] = QtGui.QIcon(f'resources/icons/{icon}')
        if os.path.isdir(f'resources/themes/{style_name}/icons'):
            for icon in os.listdir(f'resources/themes/{style_name}/icons'):
                self.icons[os.path.splitext(icon)[0]] = QtGui.QIcon(f'resources/themes/{style_name}/icons/{icon}')