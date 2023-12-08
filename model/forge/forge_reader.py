import struct
from io import BytesIO
from typing import List, Tuple

import numpy

from model.compression.compressor import Compressor
from model.files.file_data import FileData


class ForgeReader:

    NonContainerDataFiles = {16, 145}
    CompressionMarker = b"\x33\xAA\xFB\x57\x99\xFA\x04\x10"

    def __init__(self, path: str, data_file_format: int):
        self.compressor = Compressor()

        # 0=[AC1], 1=[AC2, AC2B, AC2R, AC3MP, AC4MP], 2=[AC3, AC3L, ACRo], 3=[ACU]
        self.data_file_format = data_file_format
        self.path = path

        self.forge_name = path.split('/')[-1].split('.')[0]

    def parse(self) -> list[FileData]:
        # get the data file metadata
        metadata, self._data_file_location = self._parse_forge()

        print(f"Decompressing {self.forge_name}.")
        database = {}
        for data_file_id, (data_file_resource_type, data_file_name,) in metadata.items():
            # data_file = self._data_files[data_file_id] = DataFile(data_file_id, data_file_resource_type, data_file_name)
            if data_file_resource_type == 0:
                continue
            try:
                files = self.get_decompressed_files(data_file_id)
            except:
                # traceback.print_exc()
                print(f"Error loading {self.forge_name} {data_file_id} {data_file_name}")
                continue
            assert data_file_id in files
            # in some cases the info will be in the index but not the data file (non archive formats)
            # and in some cases the info will be in the data file but not the index
            # (Brotherhood is the first game I can see with data file id in the index)
            data_file_resource_type = (
                    data_file_resource_type or files[data_file_id][0]
            )
            data_file_name = data_file_name or files[data_file_id][1]
            file_storage = {
                file_id: (file_resource_type, file_name)
                for file_id, (file_resource_type, file_name, _) in files.items()
            }
            file_storage[data_file_id] = (data_file_resource_type, data_file_name)

            database[data_file_id] = (
                data_file_resource_type,
                data_file_name,
                file_storage,
            )

        print(f"Finished decompressing {len(metadata)} data files.")

        files_data = []

        for data_file_id, (data_file_resource_type, data_file_name, file_storage) in database.items():
            data_file = FileData(data_file_name, data_file_id, 1)
            data_file.mark_as_compressed()
            files_data.append(data_file)

            for file_id, (file_resource_type, file_name) in file_storage.items():
                file_data = FileData(file_name, file_id, 2)
                file_data.mark_as_compressed()
                data_file.children.append(file_data)

        return files_data

    def get_decompressed_files(self, data_file_id):
        """Get the data file unpacked into its individual files.
        This is a dictionary that converts from the file id to the metadata and file bytes.
        Use get_decompressed_files_bytes to get just the bytes.

        :param data_file_id:
        :return:
        """
        if data_file_id in self.NonContainerDataFiles:
            raw_data = self.get_compressed_data_file(data_file_id)
            return {data_file_id: (0, "", raw_data)}
        else:
            decompressed_data = self.get_decompressed_data_file(data_file_id)
            return self._unpack_decompressed_data_file(decompressed_data)

    def get_decompressed_data_file(self, data_file_id) -> bytes:
        """Decompress and return data for a given data file as a single block of bytes.

        :param data_file_id: The numerical id of the data file
        :return: The decompressed bytes
        """
        # Start byte and offset can be found in self._data_file_location
        return self._decompress_data_file(self.get_compressed_data_file(data_file_id))

    def get_compressed_data_file(self, data_file_id) -> bytes:
        """Get the compressed packaged binary data of the data file as it appears on disk.

        :param data_file_id: The numerical id of the data file
        :return: The bytes as they appear on disk
        """
        offset, size = self._data_file_location[data_file_id]
        with open(self.path, "rb") as f:
            f.seek(offset)
            return f.read(size)

    def _parse_forge(self):
        """Parse the forge file to load metadata and data file locations."""
        print(f"Reading metadata from {self.forge_name}.")

        with open(self.path, "rb") as forge_file:
            # header
            if forge_file.read(8) != b"scimitar":
                return {}, {}
            forge_file.seek(1, 1)
            forge_file_version, file_data_header_offset = struct.unpack(
                "<iQ", forge_file.read(12)
            )
            if not 25 <= forge_file_version <= 27:
                raise Exception(
                    f'Unsupported Forge file format : "{forge_file_version}"'
                )
            self._forge_version = forge_file_version
            if forge_file_version <= 26:
                forge_file.seek(file_data_header_offset + 32)
            else:
                forge_file.seek(file_data_header_offset + 36)
            file_data_offset = struct.unpack("<q", forge_file.read(8))[0]
            forge_file.seek(file_data_offset)
            # File Data
            (
                index_count,
                index_table_offset,
                file_data_offset2,
                name_table_offset,
                raw_data_table_offset,
            ) = struct.unpack("<i4x2q8x2q", forge_file.read(48))
            forge_file.seek(index_table_offset)
            index_table: numpy.ndarray = numpy.fromfile(
                forge_file,
                [
                    ("raw_data_offset", numpy.uint64),
                    (
                        "file_id",
                        numpy.uint64 if forge_file_version >= 27 else numpy.uint32,
                    ),
                    ("raw_data_size", numpy.uint32),
                ],
                index_count,
            )
            if 25 <= forge_file_version <= 26:
                # there is a header here with not that much useful data
                index_table["raw_data_offset"] += 440

            forge_file.seek(name_table_offset)
            name_table: numpy.ndarray = numpy.fromfile(
                forge_file,
                [
                    (
                        "raw_data_size",
                        numpy.uint32,
                    ),  # This is sometimes larger than the other size. The format of these is slightly different
                    ("", numpy.uint64),
                    ("", numpy.uint32),
                    ("file_type", numpy.uint32),  # sometimes file type
                    ("", numpy.uint64),
                    ("", numpy.uint32),  # next file count
                    ("", numpy.uint32),  # previous file count
                    ("", numpy.uint32),
                    ("", numpy.uint32),  # timestamp
                    ("data_file_name", "S128"),  # usually data file name
                ]
                + [("", numpy.uint32)] * (5 if forge_file_version >= 27 else 4),
                index_count,
            )

            # assert numpy.array_equal(index_table['raw_data_size'], name_table['raw_data_size']), "The duplicated raw data sizes do not match"
            # TODO: the above sometimes do not match in games before Unity (they all match in Unity). There seems to be more compressed data after this if that is the case.

            data_file_names = name_table["data_file_name"].astype(str)
            return dict(
                zip(
                    index_table["file_id"],
                    zip(name_table["file_type"].tolist(), data_file_names),
                )
            ), dict(
                zip(
                    index_table["file_id"],
                    zip(
                        index_table["raw_data_offset"].tolist(),
                        index_table["raw_data_size"].tolist(),
                    ),
                )
            )

    def _read_compressed_data_section(
        self, raw_data_chunk: BytesIO, exhaust=True
    ) -> Tuple[int, List[bytes]]:
        """This is a helper function used in decompression"""
        raw_data_chunk.seek(2, 1)  # 01 00
        compression_type = ord(raw_data_chunk.read(1))
        raw_data_chunk.seek(2, 1)  # 00 80
        max_size = struct.unpack("<H", raw_data_chunk.read(2))[0]
        uncompressed_data_list = []
        if max_size:
            if self.data_file_format <= 2:
                comp_block_count = struct.unpack("<H", raw_data_chunk.read(2))[0]
            else:
                comp_block_count = struct.unpack("<I", raw_data_chunk.read(4))[0]
            size_table = (
                numpy.frombuffer(raw_data_chunk.read(comp_block_count * 2 * 2), "<u2")
                .reshape(-1, 2)
                .tolist()
            )  # 'uncompressed_size', 'compressed_size'
            for uncompressed_size, compressed_size in size_table:
                raw_data_chunk.seek(4, 1)  # I think this is the hash of the data
                uncompressed_data_list.append(
                    self.compressor.decompress(
                        compression_type,
                        raw_data_chunk.read(compressed_size),
                        uncompressed_size,
                    )
                )
        else:
            pointer = raw_data_chunk.tell()
            end_pointer = raw_data_chunk.seek(0, 2)
            raw_data_chunk.seek(pointer)

            while pointer < end_pointer:
                compressed = raw_data_chunk.read(1)
                if compressed == b"\x00":
                    if self.data_file_format <= 2:  # this might be wrong
                        size = struct.unpack("<H", raw_data_chunk.read(2))[0]
                    else:
                        size = struct.unpack("<I", raw_data_chunk.read(4))[0]
                    uncompressed_data_list.append(raw_data_chunk.read(size))
                elif compressed == b"\x01":
                    compressed_size, uncompressed_size, _ = struct.unpack(
                        "<3I", raw_data_chunk.read(12)
                    )
                    uncompressed_data_list.append(
                        self.compressor.decompress(
                            compression_type,
                            raw_data_chunk.read(compressed_size),
                            uncompressed_size,
                        )
                    )
                else:
                    raise Exception(
                        f"Extra metadata byte {compressed} is not recognised"
                    )
                if not exhaust:
                    break
                pointer = raw_data_chunk.tell()

        return max_size, uncompressed_data_list

    def _decompress_data_file(self, compressed_bytes: bytes) -> bytes:
        """Decompress the raw data file bytes.

        :param compressed_bytes: The bytes of the data file as they appear on disk
        :return: The decompressed bytes of the data file
        """
        if not compressed_bytes:
            # there are some files that have zero length
            return compressed_bytes

        uncompressed_data_list = []

        raw_data_chunk = BytesIO(compressed_bytes)
        if self.data_file_format == 1:
            count = struct.unpack("<I", raw_data_chunk.read(4))[0]
            if count:
                raw_data_chunk.seek(count * 8, 1)
        elif self.data_file_format == 2:
            bcount = struct.unpack("<I", raw_data_chunk.read(4))[0]
            if bcount:
                raw_data_chunk.seek(bcount, 1)
            # if self.DataFileFormat == 2:
            #     count = struct.unpack("<H", raw_data_chunk.read(2))[0]
            #     for _ in range(count):
            #         count2 = struct.unpack("<H", raw_data_chunk.read(2))[0]
            #         for _ in range(count2):
            #             assert ord(raw_data_chunk.read(1)) <= 1
            #             raw_data_chunk.seek(8, 1)  # (data?) file id
            #
            #     count = struct.unpack("<H", raw_data_chunk.read(2))[0]
            #     for _ in range(count):
            #         raw_data_chunk.seek(8, 1)  # (data?) file id
            #         raw_data_chunk.seek(1, 1)
            #         count2 = struct.unpack("<H", raw_data_chunk.read(2))[0]
            #         raw_data_chunk.seek(count2 * 2, 1)

        header = raw_data_chunk.read(8)
        if header == self.CompressionMarker:  # if compressed
            max_size, uncompressed_data_list = self._read_compressed_data_section(
                raw_data_chunk
            )
            if max_size:
                if raw_data_chunk.read(8) == self.CompressionMarker:
                    _, uncompressed_data_list_ = self._read_compressed_data_section(
                        raw_data_chunk
                    )
                    uncompressed_data_list += uncompressed_data_list_
                else:
                    raise Exception(
                        "Compression Issue. Second compression block not found"
                    )
            extra = raw_data_chunk.read()
            if extra:
                raise Exception("Compression Issue. More data found")
        else:
            raw_data_chunk_rest = header + raw_data_chunk.read()
            if self.CompressionMarker in raw_data_chunk_rest:
                raise Exception("Compression Issue")
            uncompressed_data_list.append(
                raw_data_chunk_rest
            )  # The file is not compressed

        return b"".join(uncompressed_data_list)

    def _unpack_decompressed_data_file(self, decompressed_bytes: bytes):
        files = {}

        if not decompressed_bytes:
            return files

        uncompressed_data = BytesIO(decompressed_bytes)

        data = uncompressed_data.read(2)
        file_count = struct.unpack("<H", data)[0]
        if self.data_file_format == 0:
            index_table = [
                struct.unpack("<II", uncompressed_data.read(8))
                for _ in range(file_count)
            ]
        else:
            if self.data_file_format == 1:
                fmt = "<IIh"
            elif 2 <= self.data_file_format <= 3:
                fmt = "<QIh"
            else:
                raise Exception
            fmt_len = struct.calcsize(fmt)
            index_table = []
            for _ in range(file_count):
                index_table.append(
                    struct.unpack(fmt, uncompressed_data.read(fmt_len))
                )  # file_id, data_size (file_size + header), extra16_count (for next line)
                if self.data_file_format >= 2:
                    # this may only apply to unity
                    extra16_count = index_table[-1][2]
                    if extra16_count > 0:
                        uncompressed_data.seek(extra16_count * 2, 1)
            if self._forge_version == 26:
                # AC4MP
                extra32 = struct.unpack("<I", uncompressed_data.read(4))[0]
                if extra32:
                    uncompressed_data.seek(extra32, 1)

        if self.data_file_format == 1:
            bcount = struct.unpack("<I", uncompressed_data.read(4))[0]
            uncompressed_data.seek(bcount, 1)
        for index in range(file_count):
            resource_type, file_size, file_name_size = struct.unpack(
                "<3I", uncompressed_data.read(12)
            )
            file_id = index_table[index][0]
            file_name = uncompressed_data.read(file_name_size).decode("utf-8")
            check_byte = ord(uncompressed_data.read(1))
            if check_byte == 1:
                uncompressed_data.seek(3, 1)
                unk_count = struct.unpack("<I", uncompressed_data.read(4))[0]
                uncompressed_data.seek(12 * unk_count, 1)
            elif check_byte != 0:
                raise Exception(
                    "Either something has gone wrong or a new value has been found here"
                )

            raw_file = uncompressed_data.read(file_size)

            files[file_id] = (resource_type, file_name, raw_file)
        return files
