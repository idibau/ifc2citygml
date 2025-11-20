from ifc2gml.gml.surface import Surface


class BuildingInstallation(Surface):
    def __init__(self):
        super().__init__("bldg", "BuildingInstallation")
