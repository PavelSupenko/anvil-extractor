import os
import platform


class TexturesConvertor:

    def __init__(self):
        self.library_name = 'texconv.exe'
        self.library_full_path = os.path.join(os.path.dirname(__file__), 'resources', self.library_name)

    def convert(self, args: str):
        if platform.system() != 'Windows':
            print(f'Cannot convert using DirectX library on non-Windows platforms for args: {args}')
            return

        os.system(f'{self.library_full_path} {args}')
