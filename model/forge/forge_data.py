from model.forge.forge_container_file_data import ForgeFileData, ForgeContainerFileData


class ForgeData:

    def __init__(self, version: int,
                 files_data: dict[int, ForgeContainerFileData] = {},
                 files_items_data: dict[int, ForgeFileData] = {}):

        self.files_items_data = files_items_data
        self.version = version
        self.files_data = files_data

