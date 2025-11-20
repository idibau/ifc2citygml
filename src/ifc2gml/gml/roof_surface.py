from ifc2gml.gml.surface import Surface


class RoofSurface(Surface):
    def __init__(self):
        super().__init__("con", "RoofSurface")
