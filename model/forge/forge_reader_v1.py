from model.forge.forge_reader_base import ForgeReaderBase


class ForgeReaderV1(ForgeReaderBase):

    NonContainerDataFiles = {16, 145}
    CompressionMarker = b"\x33\xAA\xFB\x57\x99\xFA\x04\x10"
    DataFileFormat = (
        0  # 0=[AC1], 1=[AC2, AC2B, AC2R, AC3MP, AC4MP], 2=[AC3, AC3L, ACRo], 3=[ACU]
    )

    def __init__(self, path: str, forge_version: int):
        super().__init__(path, forge_version)
