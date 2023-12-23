import json
import os

from model.settings.game_settings import GameSettings, GameSettingsEncoder


class GameSettingsLoader:
    GameSettingsFileName = "game_settings.json"

    def __init__(self, settings_directory_path):
        self.settings_directory_path = settings_directory_path
        self.settings_file_path = os.path.join(self.settings_directory_path, self.GameSettingsFileName)

    def load(self) -> GameSettings:
        if not os.path.exists(self.settings_file_path):
            return GameSettings()

        try:
            with open(self.settings_file_path) as f:
                settings_json = json.load(f)
                settings: GameSettings = GameSettings()
                settings.path = settings_json["path"]
                settings.preset = settings_json["preset"]
                return settings
        except:
            return GameSettings()

    def save(self, game_settings: GameSettings):
        os.makedirs(os.path.dirname(self.settings_file_path), exist_ok=True)
        with open(self.settings_file_path, 'w') as f:
            json.dump(game_settings, f, indent=4, cls=GameSettingsEncoder)
