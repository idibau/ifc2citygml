from model.city_object import CityObject


class BuildingRoom(CityObject):
    def __init__(self, ifc_element):
        super().__init__("bldg", "BuildingRoom", ifc_element)
