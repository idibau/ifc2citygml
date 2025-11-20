from ifc2gml.gml.surface import Surface


class WallSurface(Surface):
    def __init__(self):
        super().__init__("con", "WallSurface")
