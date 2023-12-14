import json
import os

from model.game.game_data import GameData


class AC2GameData(GameData):
    def __init__(self, path: str):
        file_types = json.load(open(f"{os.path.dirname(__file__)}/resource_types.json"))
        super().__init__(path, data_file_format=1, file_types=file_types)
