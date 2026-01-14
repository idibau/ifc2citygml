from model.city_object import CityObject


class BuildingFurniture(CityObject):
    def __init__(self, ifc_element):
        super().__init__("bldg", "BuildingFurniture", ifc_element)
