import os
from abc import ABC

from model.forge.forge_data import ForgeData
from model.forge.forge_file_data import ForgeFileData
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class ExportPluginBase(ABC):
    target_type = ''
    plugin_name = ''

    def __init__(self, output_directory_path: str):
        self.output_directory_path = output_directory_path

    def execute(self, forge_reader: ForgeReader, file_data: ForgeFileData, game_data: GameData):
        forge_data: ForgeData = forge_reader.forge_data
        file_id = file_data.id

        print(f'Exporting using plugin: {self.plugin_name} for file: {file_id} to directory: {self.output_directory_path}')

        if file_id not in forge_data.files_data:
            print(f'File ID {file_id} not found in forge data')
            return

        file_data: ForgeFileData = forge_data.files_data[file_id]
        print(f'File name: {file_data.name}, type: {file_data.type}, id: {file_data.id}')

        self.execute_internal(forge_reader, forge_data, file_id, file_data, game_data)

    def execute_internal(self, forge_reader: ForgeReader, forge_data: ForgeData, file_id,
                         file_data: ForgeFileData, game_data: GameData):
        raise NotImplementedError()

    # from game class get_file
    def get_file(self, forge_reader: ForgeReader, file_data: ForgeFileData, game_data: GameData):
        """Get the python class representation of a given file id.
        Will return None if the file does not exist.
        May throw an exception if parsing the file failed."""
        # file_bytes = self.get_file_bytes(file_id, forge_file, data_file_id)
        file_bytes = forge_reader.get_decompressed_files_bytes(file_data)
        file_id = file_data.id

        file_path = os.path.join(self.output_directory_path, game_data.name, f'{file_data.name}_{file_id:016X}.testformat')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        f = open(file_path, "w")
        file_wrapper = FileFormatDataWrapper(file_bytes, self, f)

        try:
            try:
                file = self.read_main_file(file_wrapper)
            except Exception as e:
                file_wrapper.clever_format()
                raise e
            if file_wrapper.clever_format():
                raise EOFError("More of file remaining")
            return file
        except Exception as e:
            stack = " > ".join(f"{rt:08X}" for rt in file_wrapper.call_stack)
            print(f"Error: {file_id:016X} Call Stack: {stack}  ---> reason ---> {e}")
            raise e
        finally:
            if f is not None:
                f.close()
