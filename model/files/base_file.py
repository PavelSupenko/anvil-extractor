from model.files.file_data_wrapper import FileDataWrapper


class BaseFile:
    ResourceType: int = None

    def read(self, file_id: int, file: FileDataWrapper):
        raise NotImplementedError

    @property
    def resource_type(self) -> int:
        """The file resource type of the file in question"""
        return self.ResourceType

    @staticmethod
    def find_sub_files(binary_data: bytes, searched_sequence: bytes):
        first_check_byte = b'\x01'
        dummy_id = b'\x00\x00\x00\x00'
        results = []

        # Find the first occurrence of the pattern
        first_occurrence = binary_data.find(searched_sequence)

        if first_occurrence != -1:
            # Ignore everything before the first match
            binary_data = binary_data[first_occurrence + 4:]

            # Split the remaining data based on the pattern
            raw_results = binary_data.split(searched_sequence)

            for result in raw_results:
                # Remove empty results
                if result:
                    results.append(first_check_byte + dummy_id + searched_sequence + result)

        return results
