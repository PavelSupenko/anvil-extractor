class ForgeFileData:
    def __init__(self, id):
        # dictionary key in general, stored for convenience
        self.id = id

        self.name = None
        self.type = None

        self.raw_data_offset = None
        self.raw_data_size = None

    def add_info(self, type, name):
        self.type = type
        self.name = name

    def add_raw_data(self, raw_data_offset, raw_data_size):
        self.raw_data_offset = raw_data_offset
        self.raw_data_size = raw_data_size
