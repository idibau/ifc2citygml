from model.city_object import CityObject


class Filling(CityObject):
    def __init__(self, namespace, tag, ifc_element):
        super().__init__(namespace, tag, ifc_element)
