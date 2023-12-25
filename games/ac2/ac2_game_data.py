import json
import os

from games.ac2.files import AC2FileReadersFactory
from model.game.game_data import GameData


class AC2GameData(GameData):
    def __init__(self, path: str):
        # file_types = json.load(open(f"{os.path.dirname(__file__)}/resource_types.json"))
        file_types = {}
        super().__init__(path=path,
                         data_file_format=1,
                         file_types=file_types,
                         file_id_datatype="I",
                         file_readers_factory=AC2FileReadersFactory())
