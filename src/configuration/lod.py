from enum import Enum

class Lod(Enum):
    """
    The available lods.
    """

    LOD_0 = "LOD_0"
    LOD_1 = "LOD_1"
    LOD_2 = "LOD_2"
    LOD_3 = "LOD_3"

    def get_lod(self):
        if self == Lod.LOD_0:
            return "lod0"
        elif self == Lod.LOD_1:
            return "lod1"
        elif self == Lod.LOD_2:
            return "lod2"
        elif self == Lod.LOD_3:
            return "lod3"
        return None