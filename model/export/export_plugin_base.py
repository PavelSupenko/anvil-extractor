from abc import ABC

from model.files.file_readers_factory_base import FileReadersFactoryBase
from model.forge.forge_data import ForgeData
from model.forge.forge_container_file_data import ForgeFileData, ForgeContainerFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportPluginBase(ABC):
    target_type = ''
    plugin_name = ''

    def __init__(self, output_directory_path: str, file_readers_factory: FileReadersFactoryBase):
        self.game_data = None
        self.file_data = None
        self.file_id = None
        self.forge_data = None
        self.forge_readers = None
        self.forge_reader = None

        self.output_directory_path = output_directory_path
        self.file_readers_factory = file_readers_factory

    def execute(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader],
                file_data: ForgeFileData, game_data: GameData):
        forge_data: ForgeData = forge_reader.forge_data
        file_id = file_data.id

        self.forge_reader = forge_reader
        self.forge_readers = forge_readers
        self.forge_data = forge_data
        self.file_id = file_id
        self.file_data = file_data
        self.game_data = game_data

        print(f'Exporting using plugin: {self.plugin_name} for file: {file_id} to directory: {self.output_directory_path}')

        if file_id in forge_data.files_data:
            file_container_data = forge_data.files_data[file_id]
            file_data: ForgeFileData = file_container_data
            print(f'File name: {file_data.name}, type: {file_data.type}, id: {file_data.id}')
            self.execute_internal(forge_reader, forge_readers, forge_data, file_id, file_data, file_container_data, game_data)
            return

        print(f'File ID {file_id} not found as a forge container file. Searching inside exporting file container...')

        file_container_data = file_data.get_top_parent_forge_item_file_data()
        if file_container_data.id in forge_data.files_data:
            print(f'File name: {file_data.name}, type: {file_data.type}, id: {file_data.id}')
            self.execute_internal(forge_reader, forge_readers, forge_data, file_id, file_data, file_container_data, game_data)
            return

        print(f'File ID {file_id} not found as a forge container file or inside exporting file container.')

    def execute_internal(self, forge_reader: ForgeReader, forge_readers: list[ForgeReader], forge_data: ForgeData,
                         file_id, file_data: ForgeFileData,  container_file_data: ForgeContainerFileData, game_data: GameData):
        raise NotImplementedError()

    def find_forge_container_file_data(self, file_id: int) -> tuple[ForgeFileData, bytes]:
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
            return file_data, file_bytes

        print(f"Failed to find file {file_id} ({file_id:016X}) as data file. Searching inside exporting file container...")

        parent_container_file = self.file_data.get_top_parent_forge_item_file_data()

        for child_file in parent_container_file.children:
            child: ForgeFileData = child_file

            # Checking top child mathc
            if child.id == file_id:
                files_bytes = forge_reader.get_decompressed_files_bytes(parent_container_file)
                file_bytes = files_bytes[file_id]
                print(f"Found file {child.name}:{file_id} inside exporting file container {parent_container_file.name}:{parent_container_file.id}")
                return child, file_bytes

        print(f"Failed to find file {file_id} ({file_id:016X}) inside exporting file container. Stop searching.")
        return None, None
