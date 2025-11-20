from lxml.etree import Element, ElementTree

from ifc2gml.gml.building import Building
from ifc2gml.gml.gml_utils import create_tag_with_namespace, create_sub_element
from ifc2gml.gml.namespace import NS


class Document:
    def __init__(self, city_model_name):
        self.city_model_name = city_model_name
        self.root = self.create_city_model()

    def create_city_model(self):
        root = Element(create_tag_with_namespace("core", "CityModel"), nsmap=NS)
        name_el = create_sub_element(root, "gml", "name")
        name_el.text = self.city_model_name
        return root

    def add_city_object_member(self, city_object_elements):
        city_object_member = create_sub_element(self.root, "core", "cityObjectMember")
        building = Building()
        building.set_id()
        city_object_member.append(building.element)
        for city_object_element in city_object_elements:
            building.add_surface(city_object_element)

    def write(self, path):
        tree = ElementTree(self.root)
        tree.write(
            path,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8"
        )
