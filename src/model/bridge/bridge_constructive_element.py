from model.city_object import CityObject
from utils.gml_utils import create_sub_element


class BridgeConstructiveElement(CityObject):
    def __init__(self, ifc_element):
        super().__init__("brid", "BridgeConstructiveElement", ifc_element)

    def add_filling(self, filling):
        parent = create_sub_element(self.element, "con", "filling")
        parent.append(filling.element)
