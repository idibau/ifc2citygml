from ifc2gml.gml.base_feature import BaseFeature


class BuildingFurniture(BaseFeature):
    def __init__(self, ifc_entity, predefined_type):
        super().__init__("bldg", "BuildingFurniture")

    def add_solid(self, solid):
        self.element.append(solid.element)
