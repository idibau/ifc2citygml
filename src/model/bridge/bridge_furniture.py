from model.city_object import CityObject


class BridgeFurniture(CityObject):
    def __init__(self, ifc_element):
        super().__init__("brid", "BridgeFurniture", ifc_element)
