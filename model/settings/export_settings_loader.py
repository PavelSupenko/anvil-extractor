import json
import os

from model.settings.export_settings import ExportSettings, ExportSettingsEncoder


class ExportSettingsLoader:
    ExportSettingsFileName = "export_settings.json"

    def __init__(self, settings_directory_path):
        self.settings_directory_path = settings_directory_path
        self.settings_file_path = os.path.join(self.settings_directory_path, self.ExportSettingsFileName)

    def load(self) -> ExportSettings:
        if not os.path.exists(self.settings_file_path):
            return ExportSettings()

        try:
            with open(self.settings_file_path) as f:
                settings_json = json.load(f)
                settings: ExportSettings = ExportSettings()
                settings.mesh_type = settings_json["mesh_type"]
                settings.texture_type = settings_json["texture_type"]
                return settings
        except:
            return ExportSettings()

    def save(self, export_settings: ExportSettings):
        os.makedirs(os.path.dirname(self.settings_file_path), exist_ok=True)
        with open(self.settings_file_path, 'w') as f:
            json.dump(export_settings, f, indent=4, cls=ExportSettingsEncoder)
