from ifc2gml.gml.surface import Surface


class ClosureSurface(Surface):
    def __init__(self):
        super().__init__("core", "ClosureSurface")
