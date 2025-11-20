from ifc2gml.gml.filling_surface import FillingSurface


class DoorSurface(FillingSurface):
    def __init__(self):
        super().__init__("con", "DoorSurface")
