from model.files.file_data_wrapper import FileDataWrapper
from model.files.material import Material
from model.forge.forge_data import ForgeData
from model.forge.forge_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class MaterialHandler:
    def __init__(self, forge_reader: ForgeReader, forge_data: ForgeData, file_id, file_data: ForgeFileData,
                 game_data: GameData, material_reader: 'BaseFile', texture_set_reader: 'BaseFile'):
        self.material_reader = material_reader
        self.texture_set_reader = texture_set_reader

        self.forge_reader = forge_reader
        self.forge_data = forge_data
        self.file_id = file_id
        self.file_data = file_data
        self.game_data = game_data

        self.materials = {}
        self.name = 'Unknown'

    def get(self, file_id: int):
        if file_id not in self.materials:
            self.materials[file_id] = self.get_material_ids(file_id)
        return self.materials[file_id]

    def get_material_ids(self, file_id: int) -> Material:
        id, name, file_bytes = self.forge_reader.get_decompressed_file(self.file_id, file_id)
        file: FileDataWrapper = FileDataWrapper(file_bytes, self.game_data)

        # Reading material set from
        self.material_reader.read(file_id, file)
        material_set_id = self.material_reader.material_set

        material_set_id, material_set_name, material_set_file_bytes = self.forge_reader.get_decompressed_file(self.file_id, material_set_id)
        if material_set_file_bytes is None:
            print(f"Failed to find file {material_set_id:016X}")
            return Material(name, missing_no=True)

        material_set_file: FileDataWrapper = FileDataWrapper(material_set_file_bytes, self.game_data)
        self.texture_set_reader.read(material_set_id, material_set_file)
        material: Material = self.texture_set_reader
        material.name = name
        return material
