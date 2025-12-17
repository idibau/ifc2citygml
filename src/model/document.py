from lxml.etree import Element, ElementTree

from model.bridge import Bridge
from model.building import Building
from utils.gml_utils import create_tag_with_namespace, create_sub_element, point_to_string
from model.namespace import NS


class Document:
    def __init__(self, city_model_name):
        self.city_model_name = city_model_name
        self.root = Element(create_tag_with_namespace("core", "CityModel"), nsmap=NS)
        name_el = create_sub_element(self.root, "gml", "name")
        name_el.text = self.city_model_name

    def add_envelope(self, min_corner, max_corner):
        bounded_by = create_sub_element(self.root, "gml", "boundedBy")
        envelope = create_sub_element(bounded_by, "gml", "Envelope")
        lower_corner = create_sub_element(envelope, "gml", "lowerCorner")
        lower_corner.text = point_to_string(min_corner)
        upper_corner = create_sub_element(envelope, "gml", "upperCorner")
        upper_corner.text = point_to_string(max_corner)

    def add_building(self, storeys, building_features):
        building = Building()
        city_object_member = create_sub_element(self.root, "core", "cityObjectMember")
        city_object_member.append(building.element)
        for storey in storeys:
            building.add_storey(storey)
        for building_feature in building_features:
            building.add_building_feature(building_feature)

    def add_bridge(self, bridge_parts, bridge_features):
        bridge = Bridge()
        city_object_member = create_sub_element(self.root, "core", "cityObjectMember")
        city_object_member.append(bridge.element)
        for bridge_part in bridge_parts:
            bridge.add_bridge_part(bridge_part)
        for bridge_feature in bridge_features:
            bridge.add_bridge_feature(bridge_feature)

    def write(self, path):
        tree = ElementTree(self.root)
        tree.write(
            path,
            pretty_print=True,
            xml_declaration=True,
            encoding="UTF-8"
        )
