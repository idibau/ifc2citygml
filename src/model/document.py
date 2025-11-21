from lxml.etree import Element, ElementTree

from model.building import Building
from utils.gml_utils import create_tag_with_namespace, create_sub_element
from model.namespace import NS


class Document:
    def __init__(self, city_model_name):
        self.city_model_name = city_model_name
        self.root = Element(create_tag_with_namespace("core", "CityModel"), nsmap=NS)
        name_el = create_sub_element(self.root, "gml", "name")
        name_el.text = self.city_model_name

    def add_building(self, building_features):
        building = Building()
        city_object_member = create_sub_element(self.root, "core", "cityObjectMember")
        city_object_member.append(building.element)
        for building_feature in building_features:
            building.add_building_feature(building_feature)

    def write(self, path):
        tree = ElementTree(self.root)
        tree.write(
            path,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8"
        )
