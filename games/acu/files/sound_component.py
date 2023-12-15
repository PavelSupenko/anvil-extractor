from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(BaseFile):
    ResourceType = 0xE8134060
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        file.read_bytes(2)
        # for _ in range(3):
        for _ in range(2):
            file.read_file()
            # SoundComponent
            # EventSwitchDependencies
        file.read_bytes(10)  # wrong but needs more examples
