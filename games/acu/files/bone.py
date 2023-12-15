from model.files.base_file import BaseFile
from model.files.file_data_wrapper import FileDataWrapper


class Reader(Bone):
    ResourceType = 0x95741049

    def __init__(
            self,
            file_id: int,
            file: FileDataWrapper
    ):
        BaseFile.__init__(self, file_id, file)
        self.bone_id = file.read_resource_type()

        if file.read_uint_8() != 3:
            self.parent_file_id = file.read_file_id()

        if file.read_uint_8() != 3:
            file.read_file_id()  # reflected file id.

        transform = file.read_numpy("float32", 16*4)

        file.read_bytes(5)
        count = file.read_uint_32()
        for _ in range(count):
            with file.indent:
                file.read_bytes(1)
                file.read_file()
        count = file.read_uint_32()
        for _ in range(count):
            with file.indent:
                file.read_resource_type()
        assert file.read_uint_32() == 7, "this should be 7"
        assert file.read_float_32() == 1, "this should be 1"  # scale factor?
        file.read_uint_16()
        file.read_uint_16()
