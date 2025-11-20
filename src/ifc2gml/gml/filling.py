from ifc2gml.gml.city_object_element import CityObjectElement
from ifc2gml.gml.gml_utils import get_solid


class Filling(CityObjectElement):
    def __init__(self, namespace, tag):
        super().__init__(namespace, tag)

    def add_solid(self, vertices, faces, lod):
        solid = get_solid(vertices, faces, lod)
        self.element.append(solid)
