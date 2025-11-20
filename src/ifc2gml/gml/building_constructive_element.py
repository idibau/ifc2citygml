from ifc2gml.gml.city_object_element import CityObjectElement
from ifc2gml.gml.gml_utils import get_solid, create_sub_element


class BuildingConstructiveElement(CityObjectElement):
    def __init__(self, class_value):
        super().__init__("bldg", "BuildingConstructiveElement")
        class_element = create_sub_element(self.element, "bldg", "class")
        class_element.text = class_value

    def add_solid(self, vertices, faces, lod):
        solid = get_solid(vertices, faces, lod)
        self.element.append(solid)

    def add_filling(self, filling):
        parent = create_sub_element(self.element, "con", "filling")
        parent.append(filling.element)
