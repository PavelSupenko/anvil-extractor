from model.files.file_data_wrapper import FileDataWrapper


class BaseFile:
    ResourceType: int = None

    def read(self, file_id: int, file: 'FileDataWrapper'):
        raise NotImplementedError

    @property
    def resource_type(self) -> int:
        """The file resource type of the file in question"""
        return self.ResourceType
