import os

from model.files.tree.system_directory_data import SystemDirectoryData
from model.files.tree.system_file_data import SystemFileData


class ForgeFilesFinder:
    def __init__(self, directory_data: SystemDirectoryData):
        self.directory_data = directory_data
        self.path = directory_data.path

    def find_files(self) -> list[SystemFileData]:
        forge_files_paths = self.find_paths()
        files_data = []

        for forge_file_path in forge_files_paths.values():
            file_data = SystemFileData(forge_file_path)
            file_data.add_parent(self.directory_data)
            files_data.append(file_data)

        return files_data

    def find_paths(self) -> dict[str, str]:
        forge_files = {}
        if os.path.isdir(self.path):
            for forge_file_name in os.listdir(self.path):
                if forge_file_name.endswith('.forge'):
                    forge_files[forge_file_name] = os.path.join(self.path, forge_file_name)

        return forge_files
