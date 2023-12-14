import json
import os


class GameData:

    def __init__(self, path: str, pre_header_length: int = 1, file_id_datatype: str = 'Q', file_type_length: int = 4):
        # TODO: Create valid files tipe injecting
        self.file_types = json.load(open(f"{os.path.dirname(__file__)}/fileFormats.json"))
        self.pre_header_length = pre_header_length
        self.file_id_datatype = file_id_datatype
        self.file_type_length = file_type_length

        self.name = path.split('/')[-1]
