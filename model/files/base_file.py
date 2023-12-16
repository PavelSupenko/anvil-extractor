class BaseFile:
    ResourceType: int = None

    @property
    def resource_type(self) -> int:
        """The file resource type of the file in question"""
        return self.ResourceType
