from model.building.building_base_feature import BuildingBaseFeature


class BuildingRoom(BuildingBaseFeature):
    def __init__(self, ifc_entity, predefined_type):
        super().__init__("bldg", "BuildingRoom")
        self.add_class(ifc_entity)

    def add_solid(self, solid):
        self.element.append(solid.element)
