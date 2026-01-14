from model.city_object import CityObject


class BuildingInstallation(CityObject):
    def __init__(self, ifc_element):
        super().__init__("bldg", "BuildingInstallation", ifc_element)
