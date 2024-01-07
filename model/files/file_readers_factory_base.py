class FileReadersFactoryBase:
    def __init__(self, file_readers: dict):
        self.file_readers: dict[int: type] = file_readers

    def get_file_reader(self, file_type: int) -> 'BaseFile':
        if file_type not in self.file_readers:
            print(f'File type {file_type} ({file_type:016X}) not supported')
            return None

        return self.file_readers[file_type]()
