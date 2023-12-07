class FileData:
    def __init__(self, name: str, file_id: int, depth: int):
        self.file_id = file_id
        self.name = name

        self.depth = depth
        self.children = []

    def __str__(self):
        return f"{self.name}\t\t{self.file_id:016X}"
