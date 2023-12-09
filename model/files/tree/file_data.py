class FileData:
    def __init__(self, path: str, file_id: int, depth: int):
        self.file_id = file_id
        self.path = path

        self.data = None

        file_name = path.split('/')[-1].split('.')
        self.name = file_name[0]
        self.type = file_name[1] if len(file_name) > 1 else None

        self.depth = depth
        self.children = []

    def __str__(self):
        return f"{self.name}\t\t{self.file_id:016X}"
