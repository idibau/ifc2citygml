from ifc2gml.gml.city_object_element import CityObjectElement
from ifc2gml.gml.gml_utils import create_sub_element


class Building(CityObjectElement):
    def __init__(self):
        super().__init__("bldg", "Building")

    def add_building_constructive_element(self, building_constructive_element):
        parent = create_sub_element(self.element, "bldg", "buildingConstructiveElement")
        parent.append(building_constructive_element.element)

    def add_surface(self, surface):
        parent = create_sub_element(self.element, "core", "boundary")
        parent.append(surface.element)


