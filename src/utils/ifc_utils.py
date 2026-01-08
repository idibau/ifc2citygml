import ifcopenshell
import ifcopenshell.util.placement as placement_util


def get_local_placement(placement):
    return placement_util.get_local_placement(placement)


def get_spatial_parent(ifc_element):
    for rel in getattr(ifc_element, "ContainedInStructure", []) or []:
        if rel.is_a("IfcRelContainedInSpatialStructure"):
            return rel.RelatingStructure
    return None


def get_building(ifc_element):
    return get_next_related_object_or_structure_of_type(ifc_element, "IfcBuilding")


def get_building_storey(ifc_element):
    return get_next_related_object_or_structure_of_type(ifc_element, "IfcBuildingStorey")


def get_bridge(ifc_element):
    return get_next_related_object_or_structure_of_type(ifc_element, "IfcBridge")


def get_bridge_part(ifc_element):
    return get_next_related_object_or_structure_of_type(ifc_element, "IfcBridgePart")


def get_next_related_object_or_structure_of_type(ifc_element, ifc_entity, visited=None):
    if visited is None:
        visited = set()
    gid = getattr(ifc_element, "GlobalId", None)
    if gid in visited:
        return None
    visited.add(gid)
    for rel in getattr(ifc_element, "ContainedInStructure", []):
        parent = rel.RelatingStructure
        if parent.is_a(ifc_entity):
            return parent
        if parent:
            element = get_next_related_object_or_structure_of_type(parent, ifc_entity, visited)
            if element:
                return element
    for rel in getattr(ifc_element, "Decomposes", []):
        parent = rel.RelatingObject
        if parent.is_a(ifc_entity):
            return parent
        if parent:
            element = get_next_related_object_or_structure_of_type(parent, ifc_entity, visited)
            if element:
                return element
    return None


def get_opening_element(ifc_element):
    fills = ifc_element.FillsVoids
    if not fills:
        return None
    opening = fills[0].RelatingOpeningElement
    voids = opening.VoidsElements
    if not voids:
        return None
    opening_element = voids[0].RelatingBuildingElement
    return opening_element


def get_pset(ifc_element, pset_name):
    return ifcopenshell.util.element.get_pset(ifc_element, pset_name)
