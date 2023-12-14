import os
from typing import Union, AnyStr, Optional


class FileObject:
	def __init__(self, path: str = None, mode: str = 'w', data: AnyStr = ''):
		self.path = path
		self.mode = mode
		self._data = data
		if path is not None:
			if 'r' in mode:
				with open(path, mode) as f:
					self._data = f.read()
			else:
				self._data = ''
				self.path = path
				self.mode = mode
		self._file_pointer = 0

	def tell(self) -> int:
		return self._file_pointer

	def write(self, s: AnyStr):
		self._data += s
		self._file_pointer += len(s)

	def read(self, length: Optional[int] = None):
		if length is None:
			data = self._data[self._file_pointer:]
			self._file_pointer = len(self._data)
			return data
		elif isinstance(length, int):
			data = self._data[self._file_pointer:self._file_pointer + length]
			self._file_pointer += length
			return data
		else:
			raise Exception(f'Unsupported entry: "{length}"')

	def seek(self, offset: int, whence: int = 0):
		if whence == 0:
			self._file_pointer = offset
		elif whence == 1:
			self._file_pointer += offset
		elif whence == 2:
			self._file_pointer = len(self._data) - offset

	def close(self, path: Union[str, None] = None, mode: Union[str, None] = None):
		if path is not None:
			self.path = path
		if mode is not None:
			self.mode = mode
		if self.mode in 'wa' and self.path is not None and self.mode is not None:
			if not os.path.isdir(os.path.dirname(self.path)):
				os.makedirs(os.path.dirname(self.path))
			with open(self.path, self.mode) as f:
				f.write(self._data)
