import json


class ExportSettings:
    def __init__(self, mesh_type="OBJ", texture_type="DDS"):
        self.mesh_type = mesh_type
        self.texture_type = texture_type


class ExportSettingsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ExportSettings):
            return obj.__dict__  # Serialize ExportSettings as a dictionary
        return json.JSONEncoder.default(self, obj)
