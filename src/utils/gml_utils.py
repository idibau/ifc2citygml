import uuid

from lxml.etree import Element, SubElement

from model.namespace import NS


def get_uuid_as_string():
    return "uuid_" + str(uuid.uuid4())


def point_to_string(point):
    return " ".join(map(str, point))


def face_to_closed_pos_list_string(vertices, face):
    coords = []
    for idx in face:
        coords.extend(map(str, vertices[idx]))
    coords.extend(map(str, vertices[face[0]]))
    return "  ".join(coords)


def create_tag_with_namespace(namespace, tag):
    return f"{{{NS[namespace]}}}{tag}"


def create_element(namespace, tag):
    return Element(create_tag_with_namespace(namespace, tag), nsmap=NS)


def create_sub_element(parent, namespace, tag):
    return SubElement(parent, create_tag_with_namespace(namespace, tag), nsmap=NS)


def create_class_value(ifc_element):
    object_type = getattr(ifc_element, "ObjectType", None)
    predefined_type = getattr(ifc_element, "PredefinedType", None)
    class_value = ifc_element.is_a()
    if predefined_type and predefined_type != "USERDEFINED":
        return f"{class_value}/{predefined_type}"
    elif object_type:
        return f"{class_value}/{object_type}"
    else:
        return class_value
