from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox

from model.settings.export_settings_loader import ExportSettingsLoader


class ExportSettingsView(QDialog):
    MeshTypes = ["OBJ", "FBX"]
    TextureTypes = ["DDS", "PNG", "JPG", "BMP"]

    def __init__(self, export_settings_loader: ExportSettingsLoader):
        QDialog.__init__(self)

        self.export_settings_loader = export_settings_loader
        self.settings = self.export_settings_loader.load()

        self.setWindowTitle("Export settings")
        self.resize(500, 200)

        self.mesh_label = QLabel("Mesh Type:")
        self.mesh_combo = QComboBox()
        self.mesh_combo.addItems(self.MeshTypes)
        self.mesh_combo.currentIndexChanged.connect(self.handle_mesh_type_changed)

        self.texture_label = QLabel("Texture Type:")
        self.texture_combo = QComboBox()
        self.texture_combo.addItems(self.TextureTypes)
        self.texture_combo.currentIndexChanged.connect(self.handle_texture_type_changed)

        self.initialize_view_items()

        layout = QVBoxLayout()
        layout.addWidget(self.mesh_label)
        layout.addWidget(self.mesh_combo)
        layout.addWidget(self.texture_label)
        layout.addWidget(self.texture_combo)

        self.setLayout(layout)

    def initialize_view_items(self):
        self.mesh_combo.setCurrentIndex(self.MeshTypes.index(self.settings.path))
        self.texture_combo.setCurrentIndex(self.TextureTypes.index(self.settings.preset))

    def handle_texture_type_changed(self, index):
        self.settings.preset = self.TextureTypes[index]

    def handle_mesh_type_changed(self, index):
        self.settings.path = self.MeshTypes[index]

        if index == 0:  # OBJ selected
            self.texture_label.setVisible(True)
            self.texture_combo.setVisible(True)
        else:
            self.texture_label.setVisible(False)
            self.texture_combo.setVisible(False)

    def save_settings(self):
        self.export_settings_loader.save(self.settings)

    def closeEvent(self, event):
        self.save_settings()
        event.accept()
