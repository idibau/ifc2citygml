from ifc2gml.gml.base_feature import BaseFeature
from ifc2gml.gml.gml_utils import create_sub_element, create_tag_with_namespace, get_uuid_as_string, \
    face_to_closed_pos_list


class Solid(BaseFeature):
    def __init__(self, lod, vertices, faces):
        super().__init__("core", f"{lod.value}Solid")
        solid = create_sub_element(self.element, "gml", "Solid")
        exterior = create_sub_element(solid, "gml", "exterior")
        shell = create_sub_element(exterior, "gml", "Shell")
        for face in faces:
            surface_member = create_sub_element(shell, "gml", "surfaceMember")
            polygon = create_sub_element(surface_member, "gml", "Polygon")
            polygon.set(create_tag_with_namespace("gml", "id"), get_uuid_as_string())
            exterior = create_sub_element(polygon, "gml", "exterior")
            linear_ring = create_sub_element(exterior, "gml", "LinearRing")
            pos_list = create_sub_element(linear_ring, "gml", "posList")
            pos_list.text = face_to_closed_pos_list(vertices, face)
            pos_list.set("srsDimension", "3")
