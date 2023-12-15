from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper
from typing import List
from pyUbiForge2.games.ACU.files.D77FB524 import Reader as Fake


class Reader(BaseFile):
    ResourceType = 0xC69A7F31
    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        fake_count = file.read_uint_32()
        self.fakes: List[Fake] = []
        for _ in range(fake_count):
            self.fakes.append(
                file.read_file()
            )
        near_fake_count = file.read_uint_32()
        self.near_fakes = []
        for _ in range(near_fake_count):
            self.near_fakes.append(
                file.read_file()
            )
        file.read_bytes(1)
