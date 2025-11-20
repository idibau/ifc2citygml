from ifc2gml.gml.city_object_element import CityObjectElement
from ifc2gml.gml.gml_utils import get_multi_surface


class FillingSurface(CityObjectElement):
    def __init__(self, namespace, tag):
        super().__init__(namespace, tag)

    def add_multi_surface(self, vertices, faces, lod):
        surface = get_multi_surface(vertices, faces, lod)
        self.element.append(surface)
