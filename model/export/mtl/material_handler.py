from model.files.file_data_wrapper import FileDataWrapper
from model.files.material import Material
from model.forge.forge_data import ForgeData
from model.forge.forge_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class MaterialHandler:
    def __init__(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], forge_data: ForgeData,
                 file_id, file_data: ForgeFileData, game_data: GameData, material_reader: 'BaseFile',
                 texture_set_reader: 'BaseFile'):

        self.material_reader = material_reader
        self.texture_set_reader = texture_set_reader

        self.forge_readers = forge_readers
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
        forge_reader, forge_container_data, material_data, material_bytes = self.get_file_data_from_any_forge(file_id)

        name = material_data.name
        file_bytes = material_bytes

        file: FileDataWrapper = FileDataWrapper(file_bytes, self.game_data)

        # Reading material set from
        self.material_reader.read(file_id, file)
        material_set_id = self.material_reader.material_set

        material_set_file_bytes = forge_reader.get_decompressed_files_bytes(forge_container_data)[material_set_id]
        if material_set_file_bytes is None:
            print(f"Failed to find file {material_set_id:016X}")
            return Material(name, missing_no=True)

        material_set_file: FileDataWrapper = FileDataWrapper(material_set_file_bytes, self.game_data)
        self.texture_set_reader.read(material_set_id, material_set_file)
        material: Material = self.texture_set_reader
        material.name = name
        return material

    # Copy of export data block plugin's method
    # Returns forge reader, forge data item, forge item and bytes
    def get_file_data_from_any_forge(self, file_id: int) -> tuple[ForgeReader, ForgeFileData, ForgeFileData, bytes]:
        forge_reader = self.forge_reader

        if file_id not in forge_reader.forge_data.files_data:
            for forge_reader_another in self.forge_readers:
                if file_id in forge_reader_another.forge_data.files_data:
                    forge_reader = forge_reader_another
                    break

        if file_id in forge_reader.forge_data.files_data:
            file_data = forge_reader.forge_data.files_data[file_id]
            files_bytes = forge_reader.get_decompressed_files_bytes(file_data)
            file_bytes = files_bytes[file_id]
            print( f'Found {file_data.name} with id {file_id} inside forge {self.forge_reader.forge_name}')
            return forge_reader, file_data, file_data, file_bytes

        print(f'Failed to find file {file_id:016X} as data file. Searching in internal files for main reader')

        forge_files: dict[int, ForgeFileData] = self.forge_reader.forge_data.files_data
        for data_file_id, data_file in forge_files.items():
            self.forge_reader.parse_file_data(data_file)

            for child_file in data_file.children:
                child: ForgeFileData = child_file

                # Checking top child mathc
                if child.id == file_id:
                    print(f'Found {child.name}:{child.id} inside {data_file.name}:{data_file.id} and forge {self.forge_reader.forge_name}')
                    file_bytes = self.forge_reader.get_decompressed_files_bytes(data_file)[file_id]
                    return self.forge_reader, data_file, child, file_bytes

        print(f'Failed to find file {file_id:016X} as data file in main reader. '
              f'Searching in internal files for all readers')

        for forge_reader in self.forge_readers:
            forge_files: dict[int, ForgeFileData] = forge_reader.forge_data.files_data
            for data_file_id, data_file in forge_files.items():
                forge_reader.parse_file_data(data_file)

                for child_file in data_file.children:
                    child: ForgeFileData = child_file

                    # Checking top child mathc
                    if child.id == file_id:
                        print(f'Found {child.name}:{child.id} inside {data_file.name}:{data_file.id} and forge {forge_reader.forge_name}')
                        file_bytes = forge_reader.get_decompressed_files_bytes(data_file)[file_id]
                        return forge_reader, data_file, child, file_bytes
