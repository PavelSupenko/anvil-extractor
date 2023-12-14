import json
import os


class GameData:

    def __init__(self, path: str, pre_header_length: int = 1, file_id_datatype: str = 'Q', file_type_length: int = 4,
                 data_file_format: int = 0, file_types: dict = None):
        # TODO: Create valid files tipe injecting
        self.file_types = file_types
        self.pre_header_length = pre_header_length
        self.file_id_datatype = file_id_datatype
        self.file_type_length = file_type_length

        # 0=[AC1], 1=[AC2, AC2B, AC2R, AC3MP, AC4MP], 2=[AC3, AC3L, ACRo], 3=[ACU]
        self.data_file_format = data_file_format

        self.name = path.split('/')[-1]
