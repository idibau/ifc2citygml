from model.city_object import CityObject


class GenericOccupiedSpace(CityObject):
    def __init__(self, ifc_element):
        super().__init__("gen", "GenericOccupiedSpace", ifc_element)
