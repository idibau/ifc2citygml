from model.city_object import CityObject


class BridgeInstallation(CityObject):
    def __init__(self, ifc_element):
        super().__init__("brid", "BridgeInstallation", ifc_element)
