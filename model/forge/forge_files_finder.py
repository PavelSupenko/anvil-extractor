import os


class ForgeFilesFinder:
    def __init__(self, path):
        self.path = path

    def find(self):
        forge_files = {}
        if os.path.isdir(self.path):
            for forge_file_name in os.listdir(self.path):
                if forge_file_name.endswith('.forge'):
                    forge_files[forge_file_name] = os.path.join(self.path, forge_file_name)

        return forge_files
