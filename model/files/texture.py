import os
import struct

from model.compression.textures_convertor import TexturesConvertor


class BaseTexture:
    def __init__(self):
        self.dwSize = b'\x7C\x00\x00\x00'  # 124
        DDSD_CAPS = DDSD_HEIGHT = DDSD_WIDTH = DDSD_PIXELFORMAT = True
        # (probably should be set based on the data)
        DDSD_PITCH = False
        DDSD_MIPMAPCOUNT = True
        DDSD_LINEARSIZE = True
        DDSD_DEPTH = False
        self.dwFlags = struct.pack(
            '<i',
            (0x1 * DDSD_CAPS) |
            (0x2 * DDSD_HEIGHT) |
            (0x4 * DDSD_WIDTH) |
            (0x8 * DDSD_PITCH) |
            (0x1000 * DDSD_PIXELFORMAT) |
            (0x20000 * DDSD_MIPMAPCOUNT) |
            (0x80000 * DDSD_LINEARSIZE) |
            (0x800000 * DDSD_DEPTH)
        )
        self.dwWidth = b'\x00\x00\x00\x00'
        self.dwHeight = b'\x00\x00\x00\x00'
        self.dwDepth = b'\x00\x00\x00\x00'
        self.imgDXT = 0
        self.dwMipMapCount = b'\x00\x00\x00\x00'
        self.dwPitchOrLinearSize = b'\x00\x00\x00\x00'
        self.buffer = b''
        self.dwReserved = b'\x00\x00\x00\x00' * 11

        self.ddspf = b''  # (pixel format)
        self.ddspf += b'\x20\x00\x00\x00'  # dwSize
        self.ddspf += b'\x00\x00\x00\x00'
        self.ddspf += b'DXT1'
        self.ddspf += b'\x00\x00\x00\x00' * 5  # dwRGBBitCount, dwRBitMask, dwGBitMask, dwBBitMask, dwABitMask
        self.DXT10Header = b''
        self.dwCaps = b'\x08\x10\x40\x00'
        self.dwCaps2 = b'\x00\x00\x00\x00'
        self.dwCaps3 = b'\x00\x00\x00\x00'
        self.dwCaps4 = b'\x00\x00\x00\x00'
        self.dwReserved2 = b'\x00\x00\x00\x00'

    # TODO: Move this functional methods away from this data class
    @property
    def dds_string(self):
        return b'DDS ' + self.dwSize + self.dwFlags + self.dwHeight + self.dwWidth + self.dwPitchOrLinearSize + \
               self.dwDepth + self.dwMipMapCount + self.dwReserved + self.ddspf + self.dwCaps + self.dwCaps2 + \
               self.dwCaps3 + self.dwCaps4 + self.dwReserved2 + self.DXT10Header + self.buffer

    def export_dds(self, path):
        with open(path, 'wb') as fi:
            fi.write(self.dds_string)

        if self.imgDXT == 8:
            arg = f'-fl 9.1 -y -o {os.path.dirname(path)} -f BC3_UNORM {path}'
            TexturesConvertor().convert(arg)
