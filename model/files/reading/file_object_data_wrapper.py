import struct
from typing import Union, IO, AnyStr

import numpy

from model.files.reading.file_object import FileObject
from model.files.reading.file_reader_handler import FileReaderHandler
from model.forge.forge_reader import ForgeReader
from model.game.game_data import GameData


class FileObjectDataWrapper:
	def __init__(self, file_object: Union[FileObject, IO], forge_reader: ForgeReader, game_data: GameData, endianness: str = '<', out_file: IO = None):
		self.game_data = game_data
		self.forge_reader = forge_reader

		self.file_object = file_object
		self._out_file = out_file
		self._indent_count = 0
		assert endianness in ('<', '>')
		self.endianness = endianness
		self.indent_chr = '\t'

	@classmethod
	def from_binary(cls, binary: bytes, forge_reader: ForgeReader, game_data: GameData, endianness: str = '<') -> 'FileObjectDataWrapper':
		return cls(FileObject(data=binary, mode='r'), forge_reader, game_data, endianness)

	@classmethod
	def from_file(cls, path: str, forge_reader: ForgeReader, game_data: GameData, endianness: str = '<') -> 'FileObjectDataWrapper':
		return cls(open(path, 'rb'), forge_reader, game_data, endianness)

	def indent(self, count: int = 1):
		self._indent_count = max(self._indent_count + count, 0)

	def bind_out_file(self, out_file: IO):
		self._out_file = out_file

	def close(self):
		self.file_object.close()
		if self._out_file is not None:
			self._out_file.close()

	def seek(self, offset: int, whence: int = 0):
		if self._out_file is None:
			self.file_object.seek(offset, whence)
		else:
			if whence == 0:  # absolute
				count = offset - self.file_object.tell()
				if count > 0:
					self._out_file.write(f'{self._indent_count * self.indent_chr}{self.hex_string(self.file_object.read(count))}\n')
				elif count < 0:
					self._out_file.write(f'Skipped back {abs(count)} bytes\n')
					self.file_object.seek(offset, whence)
			elif whence == 1:  # relative
				if offset > 0:
					self._out_file.write(f'{self._indent_count * self.indent_chr}{self.hex_string(self.file_object.read(offset))}\n')
				elif offset < 0:
					self._out_file.write(f'Skipped back {abs(offset)} bytes\n')
					self.file_object.seek(offset, whence)
			elif whence == 2:  # relative to end
				file_pointer = self.file_object.tell()
				self.file_object.seek(offset, 2)
				count = self.file_object.tell() - file_pointer
				self.file_object.seek(file_pointer)
				if count > 0:
					self._out_file.write(f'{self._indent_count * self.indent_chr}{self.hex_string(self.file_object.read(count))}\n')
				elif count < 0:
					self._out_file.write(f'Skipped back {abs(count)} bytes\n')
					self.file_object.seek(offset, whence)

	def out_file_write(self, val: AnyStr):
		if self._out_file is not None:
			self._out_file.write(f'{self._indent_count * self.indent_chr}{val}')

	def _read_struct(self, data_type: str, trailing_newline: bool = True, extra_info: bool = True):
		fmt = f'{self.endianness}{data_type}'
		num_len = struct.calcsize(fmt)
		binary = self.file_object.read(num_len)
		if len(binary) != num_len:
			raise Exception('Reached End Of File')
		val = struct.unpack(data_type, binary)[0]
		if self._out_file is not None:
			if (isinstance(val, bytes) and len(val) > 10) or not extra_info:
				self._out_file.write(
					f'{self._indent_count * self.indent_chr}{self.hex_string(binary)}'
				)
			else:
				self._out_file.write(
					f'{self._indent_count * self.indent_chr}{self.hex_string(binary)}\t\t{val}'
				)

			if trailing_newline:
				self._out_file.write('\n')
		return val

	def read_bool(self) -> bool:
		return self._read_struct('?')

	def read_int_8(self) -> int:
		return self._read_struct('b')

	def read_uint_8(self) -> int:
		return self._read_struct('B')

	def read_int_16(self) -> int:
		return self._read_struct('h')

	def read_uint_16(self) -> int:
		return self._read_struct('H')

	def read_int_32(self) -> int:
		return self._read_struct('i')

	def read_uint_32(self) -> int:
		return self._read_struct('I')

	def read_float_32(self) -> int:
		return self._read_struct('f')

	def read_int_64(self) -> int:
		return self._read_struct('q')

	def read_uint_64(self) -> int:
		return self._read_struct('Q')

	def read_bytes(self, chr_len: int) -> bytes:
		return self._read_struct(f'{chr_len}s')

	def read_id(self) -> int:
		file_id = self._read_struct(self.game_data.file_id_datatype, False, False)
		if self._out_file is not None:
			# data = pyUbiForge.temp_files(file_id)
			additional_data = self.forge_reader.forge_data.files_data[file_id]
			data = self.forge_reader.get_decompressed_data_file(file_id)
			if data is None:
				self._out_file.write('\t\tUnknown File ID\n')
			else:
				#self._out_file.write(f'\t\t{data.file_name}\t{data.file_type}\n'.format(data=data))
				self._out_file.write(f'\t\t{additional_data.name}\t{additional_data.type}\n'.format(data=data))
		return file_id

	def read_type(self) -> str:
		binary = self.file_object.read(self.game_data.file_type_length)
		if len(binary) != self.game_data.file_type_length:
			raise Exception('Reached End Of File')
		file_type = ''.join(f'{b:02X}' for b in binary[::-1])
		if self._out_file is not None:
			self._out_file.write(f'{self._indent_count * self.indent_chr}{self.hex_string(binary)}\t\t{file_type}\t{self.game_data.file_types.get(file_type, "Undefined")}\n')
		return file_type

	def read_struct(self, data_types: str):
		# data_types should not be prefixed with the endianness (this is added on for you)
		fmt = f'{self.endianness}{data_types}'
		binary = self.file_object.read(struct.calcsize(fmt))
		if len(binary) != struct.calcsize(fmt):
			raise Exception('Reached End Of File')
		val = struct.unpack(fmt, binary)
		if self._out_file is not None:
			self._out_file.write(f'{self._indent_count * self.indent_chr}{self.hex_string(binary)}\t\t{val}\n')
		return val

	def read_numpy(self, dtype, binary_size: int):
		binary = self.file_object.read(binary_size)
		if len(binary) != binary_size:
			raise Exception('Reached End Of File')
		val = numpy.fromstring(binary, dtype)
		if self._out_file is not None:
			self._out_file.write(f'{self._indent_count * self.indent_chr}{self.hex_string(binary)}\t\t{val}\n')
		return val

	def read_file(self):
		# return pyUbiForge.read_file.get_data_recursive(self)
		return FileReaderHandler(game_data=self.game_data).get_data(self)

	def read_rest(self) -> bytes:
		binary = self.file_object.read()
		if self._out_file is not None:
			self._out_file.write(f'{self._indent_count * self.indent_chr}{self.hex_string(binary)}\n')
		return binary

	def hex_string(self, binary: bytes) -> str:
		return ' '.join(f'{b:02X}' for b in binary)

	def clever_format(self):
		if self._out_file is not None:
			hex_str = []
			might_be_a_file_type = ''.join(f'{b:02X}' for b in self.file_object.read(4)[::-1])
			while len(might_be_a_file_type) == 8:
				if might_be_a_file_type in self.game_data.file_types:
					self._out_file.write(f'{self._indent_count * self.indent_chr}{" ".join(hex_str)}\n')
					self._out_file.write(f'{self._indent_count * self.indent_chr}{might_be_a_file_type}\t\t{self.game_data.file_types.get(might_be_a_file_type)}\n')
					hex_str = []
					might_be_a_file_type = ''.join(f'{b:02X}' for b in self.file_object.read(4)[::-1])
				else:
					hex_str.append(might_be_a_file_type[6:])
					next_chr = self.file_object.read(1)
					if next_chr == b'':
						might_be_a_file_type = might_be_a_file_type[:6]
					else:
						might_be_a_file_type = f'{next_chr[0]:02X}{might_be_a_file_type[:6]}'

			while might_be_a_file_type != '':
				hex_str.append(might_be_a_file_type[-2:])
				might_be_a_file_type = might_be_a_file_type[:-2]
			self._out_file.write(f'{self._indent_count * self.indent_chr}{" ".join(hex_str)}\n')
		return
