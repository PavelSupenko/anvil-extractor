import struct
from io import BytesIO
from typing import List, Tuple, Any, Union

import numpy

from model.files.base_file import BaseFile
from model.files.indent import Indent
from model.game.game_data import GameData


class FileDataWrapper(BytesIO):
    def __init__(
            self,
            file: bytes,
            game_data: GameData
    ):
        assert isinstance(file, bytes), "File must be bytes"
        assert game_data.endianness in ('<', '>'), "Endianness marker must be \"<\" or \">\""
        super().__init__(file)
        self._game_data = game_data
        self._endianness = game_data.endianness
        self._call_stack: List[int] = []

        self.read_pre_data_header()

    def read_pre_data_header(self):
        header = self.read_uint_8()
        assert header == 1, "Expected the first byte to be 1"
        file_id = self.read_file_id()
        resource_type = self.read_resource_type()

    @property
    def indent(self):
        """with file.indent:"""
        return Indent()

    @property
    def call_stack(self) -> List[int]:
        return self._call_stack

    def out_file_write(self, val: str):
        pass

    def _read_struct(self, data_type: str) -> Tuple[Any]:
        fmt = f'{self._endianness}{data_type}'
        num_len = struct.calcsize(fmt)
        binary = self.read(num_len)
        if len(binary) != num_len:
            raise IOError('Reached End Of File')
        return struct.unpack(fmt, binary)

    def read_struct(self, data_types: str) -> Tuple[Any]:
        # data_types should not be prefixed with the endianness (this is added on for you)
        return self._read_struct(data_types)

    def read_bool(self) -> bool:
        return self._read_struct('?')[0]

    def read_int_8(self) -> int:
        return self._read_struct('b')[0]

    def read_uint_8(self) -> int:
        return self._read_struct('B')[0]

    def read_int_16(self) -> int:
        return self._read_struct('h')[0]

    def read_uint_16(self) -> int:
        return self._read_struct('H')[0]

    def read_int_32(self) -> int:
        return self._read_struct('i')[0]

    def read_uint_32(self) -> int:
        return self._read_struct('I')[0]

    def read_float_32(self) -> int:
        return self._read_struct('f')[0]

    def read_int_64(self) -> int:
        return self._read_struct('q')[0]

    def read_uint_64(self) -> int:
        return self._read_struct('Q')[0]

    def read_bytes(self, chr_len: int) -> bytes:
        return self._read_struct(f'{chr_len}s')[0]

    def read_file_id(self) -> int:
        return self._read_struct(self._game_data.file_id_datatype)[0]

    def read_resource_type(self) -> int:
        return self._read_struct(self._game_data.resource_d_type)[0]

    def read_numpy(self, dtype, binary_size: int) -> numpy.ndarray:
        binary = self.read(binary_size)
        if len(binary) != binary_size:
            raise IOError('Reached End Of File')
        return numpy.copy(numpy.frombuffer(binary, dtype))

    def read_rest(self) -> bytes:
        return self.read()

    def clever_format(self):
        return self.read()

    # TODO: below methods is from game class of original project. Should be moved elsewhere

    def read_main_file(self) -> "BaseFile":
        assert self.read_uint_8() == 1, "Expected the first byte to be 1"
        return self.read_file()

    def read_header_file(self) -> Union["BaseFile", int]:
        """Read a file with an extra byte before."""
        switch = self.read_uint_8()
        if switch == 0:
            return self.read_file()
        elif switch == 2:
            count = self.read_uint_32()
            raise NotImplementedError("Header switch == 2")  # might be nothing
        elif switch == 3:
            return 0
        else:
            raise NotImplementedError(f"Header switch == {switch}")

    def read_file_switch(self) -> Union["BaseFile", int]:
        switch = self.read_uint_8()
        if switch == 0:
            return self.read_header_file()
        elif 1 <= switch <= 2:
            return self.read_file_id()
        elif switch == 3:
            return 0
        elif switch == 4:
            return self.read_header_file()
        elif switch == 5:
            return self.read_file_id()
        raise Exception("I am not quite sure what to do here.")

    def read_file(self) -> "BaseFile":
        """Read a file id, resource type and the file payload and return the data packed into a class."""
        file_id = self.read_file_id()
        resource_type = self.read_resource_type()
        return self.read_file_data(file_id, resource_type)

    def read_file_data(self, file_id: int, resource_type: int) -> "BaseFile":
        """Read the file payload for a given resource type."""
        self.call_stack.append(resource_type)
        self._game_data.file_readers_factory.get_file_reader(resource_type)

        if resource_type in self._game_data.file_readers:
            reader: BaseFile = self._game_data.file_readers[resource_type]()
            data = reader.read(file_id, self)
        else:
            raise TypeError(f"{resource_type:08X}")
        self.call_stack.pop()
        return data
