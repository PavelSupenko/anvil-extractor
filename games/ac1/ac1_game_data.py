import json
import os

from games.ac1.files import AC1FileReadersFactory
from model.game.game_data import GameData


class AC1GameData(GameData):
    def __init__(self, path: str):
        # file_types = json.load(open(f"{os.path.dirname(__file__)}/resource_types.json"))
        file_types = {}
        super().__init__(path=path,
                         data_file_format=1,
                         file_types=file_types,
                         file_id_datatype="I",
                         file_readers_factory=AC1FileReadersFactory())
