import uuid

from lxml.etree import Element, SubElement

from ifc2gml.gml.namespace import NS


def get_uuid_as_string():
    return "uuid_" + str(uuid.uuid4())


def get_multi_surface(vertices, faces, lod):
    lod_x_multi_surface = create_element("core", f"{lod.value}MultiSurface")
    multi_surface = create_sub_element(lod_x_multi_surface, "gml", "MultiSurface")
    for face in faces:
        surface_member = create_sub_element(multi_surface, "gml", "surfaceMember")
        polygon = create_sub_element(surface_member, "gml", "Polygon")
        polygon.set(create_tag_with_namespace("gml", "id"), get_uuid_as_string())
        exterior = create_sub_element(polygon, "gml", "exterior")
        linear_ring = create_sub_element(exterior, "gml", "LinearRing")
        pos_list = create_sub_element(linear_ring, "gml", "posList")
        pos_list.text = face_to_closed_pos_list(vertices, face)
        pos_list.set("srsDimension", "3")
    return lod_x_multi_surface


def get_solid(vertices, faces, lod):
    lod_x_solid = create_element("core", f"{lod.value}Solid")
    solid = create_sub_element(lod_x_solid, "gml", "Solid")
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
    return lod_x_solid


def face_to_closed_pos_list(vertices, face):
    coords = []
    for idx in face:
        coords.extend(map(str, vertices[idx]))
    coords.extend(map(str, vertices[face[0]]))
    return "  ".join(coords)

def create_tag_with_namespace(namespace, tag):
    return f"{{{NS[namespace]}}}{tag}"

def create_element(namespace, tag):
    return Element(create_tag_with_namespace(namespace, tag))


def create_sub_element(parent, namespace, tag):
    return SubElement(parent, create_tag_with_namespace(namespace, tag))
