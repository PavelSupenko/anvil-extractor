from model.forge.forge_file_data import ForgeFileData


class ForgeData:

    def __init__(self, version: int, files_data: dict[int, ForgeFileData]):
        self.version = version
        self.files_data = files_data

