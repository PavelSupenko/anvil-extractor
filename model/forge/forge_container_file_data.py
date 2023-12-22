from model.forge.forge_file_data import ForgeFileData


class ForgeContainerFileData(ForgeFileData):
    def __init__(self, id):
        super().__init__(id)
        self.raw_data_offset = ''
        self.raw_data_size = ''

    def add_raw_data(self, raw_data_offset, raw_data_size):
        self.raw_data_offset = raw_data_offset
        self.raw_data_size = raw_data_size

    @property
    def properties(self) -> list[str]:
        return [self.name, self.type, self.id, self.raw_data_offset, self.raw_data_size]
        # return [self.name, f'{self.type:016X}', self.id, self.raw_data_offset, self.raw_data_size]
