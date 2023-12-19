class FileReadersFactoryBase:
    def __init__(self, file_readers: dict):
        self.file_readers: dict[int: type] = file_readers

    def get_file_reader(self, file_type: int) -> 'BaseFile':
        return self.file_readers[file_type]()
