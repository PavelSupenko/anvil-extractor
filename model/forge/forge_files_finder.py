import os

from model.files.tree.system_file_data import SystemFileData


class ForgeFilesFinder:
    def __init__(self, path):
        self.path = path

    def find_files(self) -> list[SystemFileData]:
        forge_files = self.find_paths()
        files_data = []

        for forge_file_path in forge_files.values():
            files_data.append(SystemFileData(forge_file_path))

        return files_data

    def find_paths(self) -> dict[str, str]:
        forge_files = {}
        if os.path.isdir(self.path):
            for forge_file_name in os.listdir(self.path):
                if forge_file_name.endswith('.forge'):
                    forge_files[forge_file_name] = os.path.join(self.path, forge_file_name)

        return forge_files
