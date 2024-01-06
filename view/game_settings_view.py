from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QFileDialog, QPushButton

from model.settings.game_settings_loader import GameSettingsLoader


class GameSettingsView(QDialog):
    PresetTypes = ["AC1", "AC2", "ACU", "Custom"]

    def __init__(self, game_settings_loader: GameSettingsLoader):
        QDialog.__init__(self)

        self.game_settings_loader = game_settings_loader
        self.settings = self.game_settings_loader.load()

        self.setWindowTitle("Game settings")
        self.resize(700, 200)

        self.game_directory_label = QLabel("Game Directory:")
        self.game_directory_button = QPushButton("Choose Game Directory")
        self.game_directory_button.clicked.connect(self.handle_directory_changed)

        self.preset_label = QLabel("Preset:")
        self.preset_combo = QComboBox()
        self.preset_combo.addItems(self.PresetTypes)
        self.preset_combo.currentIndexChanged.connect(self.handle_preset_type_changed)

        self.initialize_view_items()

        layout = QVBoxLayout()
        layout.addWidget(self.game_directory_label)
        layout.addWidget(self.game_directory_button)
        layout.addWidget(self.preset_label)
        layout.addWidget(self.preset_combo)

        self.setLayout(layout)

    def initialize_view_items(self):
        if self.settings.path is not None:
            self.game_directory_button.setText(self.settings.path)

        if self.settings.preset is not None:
            self.preset_combo.setCurrentIndex(self.PresetTypes.index(self.settings.preset))

    def handle_directory_changed(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Game Directory")
        if directory:
            self.settings.path = directory
            self.game_directory_button.setText(directory)

    def handle_preset_type_changed(self, index):
        self.settings.preset = self.PresetTypes[index]

    def save_settings(self):
        self.game_settings_loader.save(self.settings)

    def closeEvent(self, event):
        self.save_settings()
        event.accept()
