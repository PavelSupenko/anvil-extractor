import logging
from typing import TextIO, Union

from model.files.type_readers import default_type_readers

from model.files.reading.file_object_data_wrapper import FileObjectDataWrapper
from model.game.game_data import GameData


class FileReaderHandler:
    def __init__(self, game_data: GameData):
        self.game_data = game_data
        self.readers = {}

        for instance in default_type_readers:
            self.readers[instance.file_type] = instance

    def get_data(self, file_object_data_wrapper: FileObjectDataWrapper,
                 out_file: Union[None, FileObjectDataWrapper, TextIO] = None):
        """Call this function in the right click methods as the start point
        Will call get_data_recursive to get the actual data followed by the clever_format method to read the rest of the file
        :param file_object_data_wrapper: The input raw data
        :return: objects defined in the plugins
        """

        file_object_data_wrapper.bind_out_file(out_file)
        if not isinstance(file_object_data_wrapper, FileObjectDataWrapper):
            raise Exception('file_object_data_wrapper is not of type FileObjectDataWrapper')
        file_object_data_wrapper.read_bytes(self.game_data.pre_header_length)
        try:
            data = self.get_data_recursive(file_object_data_wrapper)
        except Exception as e:
            logging.warning(str(e))
            data = None
        file_object_data_wrapper.clever_format()
        return data

    def get_data_recursive(self, file_object_data_wrapper: FileObjectDataWrapper):
        """
        Call this function in file reader methods to access other file types in the same file
        :param file_object_data_wrapper: The input raw data
        :return: objects defined in the plugins
        """

        file_object_data_wrapper.out_file_write('\n')
        file_id = file_object_data_wrapper.read_id()
        file_type = file_object_data_wrapper.read_type()
        if file_type in self.readers:
            file_object_data_wrapper.indent()
            ret = self.readers[file_type](file_object_data_wrapper)
            ret.file_id = file_id
            file_object_data_wrapper.indent(-1)
            return ret
        else:
            raise Exception(f'File type {file_type} does not have a file reader')
