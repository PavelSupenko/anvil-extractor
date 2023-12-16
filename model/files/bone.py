from typing import Optional

from model.files.base_file import BaseFile


class Bone(BaseFile):
    parent_file_id: Optional[int] = None
    