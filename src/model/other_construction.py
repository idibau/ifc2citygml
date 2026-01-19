from model.city_object import CityObject


class OtherConstruction(CityObject):
    def __init__(self, ifc_element):
        super().__init__("con", "OtherConstruction", ifc_element)
