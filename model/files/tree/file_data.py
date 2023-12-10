class FileData:
    def __init__(self, path: str, file_id: int, depth: int, file_type=None):
        self.file_id = file_id
        self.path = path

        file_name = path.split('/')[-1].split('.')
        self.name = file_name[0]

        type_from_path = file_name[1] if len(file_name) > 1 else None
        self.type = type_from_path if file_type is None else file_type

        # tree data
        self.depth = depth
        self.parent: FileData = None
        self.children: list[FileData] = []

    def __str__(self):
        return f"{self.name} - id:{self.file_id:016X}, type:{self.type}"
