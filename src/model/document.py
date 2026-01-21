from lxml import etree

from model.namespace import NS
from utils.gml_utils import create_tag_with_namespace, point_to_string, create_sub_element, create_element


class Document:
    def __init__(self, city_model_name, filepath):
        self.filepath = filepath
        self.city_model_name = city_model_name
        self.xf = etree.xmlfile(filepath, encoding="UTF-8")
        self.xf_ctx = self.xf.__enter__()
        self.xf_ctx.write_declaration()
        self.root = self.xf_ctx.element(create_tag_with_namespace("core", "CityModel"), nsmap=NS)
        self.root.__enter__()
        self._write_name()

    def _write_name(self):
        name_el = create_element("gml", "name")
        name_el.text = self.city_model_name
        self.xf_ctx.write(name_el, pretty_print=True)

    def add_envelope(self, min_corner, max_corner, srs_name):
        bounded_by = create_element("gml", "boundedBy")
        envelope = create_sub_element(bounded_by, "gml", "Envelope")
        if srs_name:
            envelope.set("srsName", srs_name)
        lower_corner = create_sub_element(envelope, "gml", "lowerCorner")
        lower_corner.text = point_to_string(min_corner)
        upper_corner = create_sub_element(envelope, "gml", "upperCorner")
        upper_corner.text = point_to_string(max_corner)
        self.xf_ctx.write(bounded_by, pretty_print=True)

    def add_building(self, building):
        city_object_member = create_element("core", "cityObjectMember")
        city_object_member.append(building.element)
        self.xf_ctx.write(city_object_member, pretty_print=True)

    def add_bridge(self, bridge):
        city_object_member = create_element("core", "cityObjectMember")
        city_object_member.append(bridge.element)
        self.xf_ctx.write(city_object_member, pretty_print=True)

    def add_generic(self, generic_feature):
        city_object_member = create_element("core", "cityObjectMember")
        city_object_member.append(generic_feature.element)
        self.xf_ctx.write(city_object_member, pretty_print=True)

    def close(self):
        self.root.__exit__(None, None, None)
        self.xf.__exit__(None, None, None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
