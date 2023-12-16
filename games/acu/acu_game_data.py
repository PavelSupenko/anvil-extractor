import json
import os

from games.acu.files import ACUFileReadersFactory
from model.game.game_data import GameData


class ACUGameData(GameData):
    def __init__(self, path: str):
        file_types = json.load(open(f"{os.path.dirname(__file__)}/resource_types.json"))
        super().__init__(path=path,
                         data_file_format=3,
                         file_types=file_types,
                         file_readers_factory=ACUFileReadersFactory)
