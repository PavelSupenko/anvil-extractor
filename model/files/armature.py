from typing import Dict, Any

from model.files.base_file import BaseFile
from model.files.bone import Bone


class Armature(BaseFile):
    bones: Dict[int, Bone] = {}

    def extend(self, *armature: "Armature") -> "Armature":
        """Create a new armature that is the combination of the armatures"""
        new_armature = Armature(self.file_id, self.resource_type)
        new_armature.bones = self.bones.copy()
        for a in armature:
            new_armature.bones.update(a.bones)
        return new_armature

    def hierarchy(self) -> Dict[int, Dict[int, Any]]:
        hierarchy = {}
        for bone_id, bone in self.bones.items():
            hierarchy.setdefault(bone.parent_file_id, {})[bone.file_id] = {}

        nested_bones = set()
        for bone, sub_bones in hierarchy.items():
            for sub_bone in sub_bones:
                if sub_bone in hierarchy:
                    sub_bones[sub_bone] = hierarchy[sub_bone]
                    nested_bones.add(sub_bone)

        for bone in nested_bones:
            del hierarchy[bone]

        return hierarchy
