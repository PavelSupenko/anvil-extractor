import json


class GameSettings:
    def __init__(self, path = None, preset = None):
        self.path = path
        self.preset = preset

    @property
    def is_valid(self):
        return self.path is not None and self.preset is not None


class GameSettingsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, GameSettings):
            return obj.__dict__  # Serialize ExportSettings as a dictionary
        return json.JSONEncoder.default(self, obj)
