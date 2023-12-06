from typing import Dict, Union, Tuple, List, Optional
from PySide6 import QtWidgets, QtGui, QtCore


class PluginOptionsScreen(QtWidgets.QDialog):
    def __init__(self: pyUbiForge, plugin_name: str, screen: Dict[str, dict]):
        QtWidgets.QDialog.__init__(self)
        self.setModal(True)
        self._screen = screen
        self._options = {}
        self._labels = []
        self._escape = False
        self.setWindowTitle(plugin_name)
        self.setWindowIcon(QtGui.QIcon('icon.ico'))

        self._vertical_layout = QtWidgets.QVBoxLayout()
        self._vertical_layout.setObjectName("verticalLayout")
        self.setLayout(self._vertical_layout)

        self._horizontal_layouts = []

        for option_name, option in screen.items():
            option_type = option.get('type', None)
            self._horizontal_layouts.append(QtWidgets.QHBoxLayout())
            self._vertical_layout.addLayout(self._horizontal_layouts[-1])
            self._labels.append(QtWidgets.QLabel())
            self._labels[-1].setText(option_name)
            self._horizontal_layouts[-1].addWidget(self._labels[-1])
            if option_type == 'select':
                selection = [str(op) for op in option.get('options', [])]
                self._options[option_name] = QtWidgets.QComboBox()
                self._options[option_name].addItems(selection)
                self._horizontal_layouts[-1].addWidget(self._options[option_name])
            elif option_type == 'str_entry':
                self._options[option_name] = QtWidgets.QLineEdit()
                self._options[option_name].setText(option.get('default', ''))
                self._horizontal_layouts[-1].addWidget(self._options[option_name])
            elif option_type == 'int_entry':
                self._options[option_name] = QtWidgets.QSpinBox()
                val = option.get('default', 0)
                if not isinstance(val, int):
                    val = 0
                if isinstance(option.get('min', None), int):
                    self._options[option_name].setMinimum(option.get('min'))
                else:
                    self._options[option_name].setMinimum(-999999999)
                if isinstance(option.get('max', None), int):
                    self._options[option_name].setMaximum(option.get('max'))
                else:
                    self._options[option_name].setMaximum(999999999)
                self._options[option_name].setValue(val)
                self._horizontal_layouts[-1].addWidget(self._options[option_name])
            elif option_type == 'float_entry':
                self._options[option_name] = QtWidgets.QDoubleSpinBox()
                self._options[option_name].setDecimals(10)
                val = option.get('default', 0.0)
                if isinstance(val, int):
                    val = float(val)
                elif not isinstance(val, float):
                    val = 0.0
                if isinstance(option.get('min', None), (int, float)):
                    self._options[option_name].setMinimum(float(option.get('min')))
                else:
                    self._options[option_name].setMinimum(float('-Inf'))
                if isinstance(option.get('max', None), (int, float)):
                    self._options[option_name].setMaximum(float(option.get('max')))
                else:
                    self._options[option_name].setMaximum(float('Inf'))
                self._options[option_name].setValue(val)
                self._horizontal_layouts[-1].addWidget(self._options[option_name])
            elif option_name == 'check_box':
                self._options[option_name] = QtWidgets.QCheckBox()
                self._options[option_name].setChecked(option.get('default', True))
                self._horizontal_layouts[-1].addWidget(self._options[option_name])
            elif option_type == 'dir_select':
                self.create_dialog_button(option_name, option, 'dir')
            elif option_type == 'file_select':
                self.create_dialog_button(option_name, option, 'file')

        self._horizontal_layouts.append(QtWidgets.QHBoxLayout())
        self._vertical_layout.addLayout(self._horizontal_layouts[-1])

        self._okay_button = QtWidgets.QPushButton('OK')
        self._okay_button.clicked.connect(lambda: self.done(1))
        self._cancel_button = QtWidgets.QPushButton('Cancel')
        self._cancel_button.clicked.connect(self.reject)
        self._horizontal_layouts[-1].addWidget(self._okay_button)
        self._horizontal_layouts[-1].addWidget(self._cancel_button)

        self.show()
        self.exec()

    def reject(self):
        self._escape = True
        QtWidgets.QDialog.reject(self)

    @property
    def options(self) -> Dict[str, Union[str, int, float]]:
        options = {}
        for option_name, var in self._options.items():
            if isinstance(var, QtWidgets.QComboBox):
                options[option_name] = self._screen[option_name]['options'][var.currentIndex()]
            elif isinstance(var, QtWidgets.QLineEdit):
                options[option_name] = var.text()
            elif isinstance(var, QtWidgets.QSpinBox):
                options[option_name] = var.value()
            elif isinstance(var, QtWidgets.QDoubleSpinBox):
                options[option_name] = var.value()
            elif isinstance(var, QtWidgets.QCheckBox):
                options[option_name] = var.isChecked()
            elif isinstance(var, QtWidgets.QPushButton):
                options[option_name] = var.text()
        return options

    @property
    def escape(self) -> bool:
        return self._escape

    def create_dialog_button(self, option_name: str, option: dict, mode: str):
        self._options[option_name] = QtWidgets.QPushButton()
        if "default" in option and isinstance(option["default"], str):
            path = option["default"]
        else:
            path = self._pyUbiForge.CONFIG.get("dumpFolder")
        self._options[option_name].setText(path)
        self._options[option_name].clicked.connect(lambda: self.open_dialog(option_name, mode, path))
        self._horizontal_layouts[-1].addWidget(self._options[option_name])

    def open_dialog(self, option_name: str, mode: str, path: str):
        text = None
        if mode == 'dir':
            text = QtWidgets.QFileDialog.getExistingDirectory(self, "Open Directory", path)
        elif mode == 'file':
            text = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", path)
            if text != '':
                text = text[0]

        if text != '':
            self._options[option_name].setText(text)
