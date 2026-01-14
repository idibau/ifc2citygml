from model.city_object import CityObject


class BridgeRoom(CityObject):
    def __init__(self, ifc_element):
        super().__init__("brid", "BridgeRoom", ifc_element)
