from ifc2gml.gml.filling_surface import FillingSurface


class WindowSurface(FillingSurface):
    def __init__(self):
        super().__init__("con", "WindowSurface")
