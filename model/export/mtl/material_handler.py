from model.files.file_data_wrapper import FileDataWrapper
from model.files.file_readers_factory_base import FileReadersFactoryBase
from model.files.material import Material
from model.forge.forge_data import ForgeData
from model.forge.forge_container_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class MaterialHandler:
    def __init__(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], forge_data: ForgeData,
                 file_id, file_data: ForgeFileData, game_data: GameData, file_readers_factory: FileReadersFactoryBase):

        self.file_readers_factory = file_readers_factory
        self.material_id = 0x85C817C3
        self.texture_id = 0xD70E6670

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
        forge_reader, forge_container_data, material_data, material_bytes = self.get_forge_container_file_data(file_id)

        if material_data is None:
            print(f"Failed to find file {file_id:016X}")
            return Material(f'{file_id:016X}', missing_no=True)

        name = material_data.name
        file_bytes = material_bytes

        file: FileDataWrapper = FileDataWrapper(file_bytes, self.game_data)

        # Reading material set from
        material_reader = self.file_readers_factory.get_file_reader(self.material_id)
        material_reader.read(file_id, file)
        material_set_id = material_reader.material_set

        forge_reader, forge_container_data, material_data, material_bytes = self.get_forge_container_file_data(material_set_id)

        if material_bytes is None:
            print(f"Failed to find file {material_set_id}. Bytes array is None")
            return Material(name, missing_no=True)

        material_set_file: FileDataWrapper = FileDataWrapper(material_bytes, self.game_data)

        texture_set_reader = self.file_readers_factory.get_file_reader(self.texture_id)
        texture_set_reader.read(material_set_id, material_set_file)
        material: Material = texture_set_reader
        material.name = name
        return material

    def get_forge_container_file_data(self, file_id: int) -> tuple[ForgeReader, ForgeFileData, ForgeFileData, bytes]:
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
            print(f"Found file {file_id} as data file in {forge_reader.forge_name}")
            return forge_reader, file_data, file_data, file_bytes

        print(f"Failed to find file {file_id:016X} as data file. Searching inside exporting file container...")

        parent_container_file = self.file_data.get_top_parent_forge_item_file_data()

        for child_file in parent_container_file.children:
            child: ForgeFileData = child_file

            # Checking top child match
            if child.id == file_id:
                files_bytes = forge_reader.get_decompressed_files_bytes(self.file_data)
                file_bytes = files_bytes[file_id]
                print(f"Found file {child.name}:{file_id} inside exporting file container {parent_container_file.name}:{parent_container_file.id}")
                return forge_reader, parent_container_file, child, file_bytes

        print(f"Failed to find file {file_id:016X} inside exporting file container. Stop searching.")
        return None, None, None, None
