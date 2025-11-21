import ifcopenshell.util.placement as placement_util
import numpy as np


def get_local_matrix(placement):
    """Return 4x4 local transform for a placement, or identity if unsupported."""
    return placement_util.get_local_placement(placement)


def get_parent_placement(placement):
    """Return the parent placement, handling Local and Linear placements."""
    if not placement:
        return None
    if placement.is_a("IfcLocalPlacement"):
        return getattr(placement, "PlacementRelTo", None)
    elif placement.is_a("IfcLinearPlacement"):
        return getattr(placement, "PositionedRelativeTo", None)
    else:
        return None


def get_absolute_placement(placement):
    """Traverse PlacementRelTo recursively to world coordinates."""
    mats = []
    while placement:
        mats.append(get_local_matrix(placement))
        placement = getattr(placement, "PlacementRelTo", None)

    total = np.eye(4)
    for m in reversed(mats):  # parent first
        total = total @ m
    return total


def get_spatial_parent(product):
    """Return the nearest spatial structure element containing the product."""
    for rel in getattr(product, "ContainedInStructure", []) or []:
        if rel.is_a("IfcRelContainedInSpatialStructure"):
            return rel.RelatingStructure
    return None


def get_building_recursive(ifc_product, visited=None):
    """
    Recursively find the IfcBuilding that contains this product,
    traversing spatial structure and decomposition relations.
    """
    if visited is None:
        visited = set()

    # Use GlobalId if available, otherwise fallback to Python id
    gid = getattr(ifc_product, "GlobalId", None) or id(ifc_product)
    if gid in visited:
        return None
    visited.add(gid)

    for rel in getattr(ifc_product, "ContainedInStructure", []) or []:
        if not rel.is_a("IfcRelContainedInSpatialStructure"):
            continue
        parent = rel.RelatingStructure
        if parent.is_a("IfcBuilding"):
            return parent
        if parent:
            building = get_building_recursive(parent, visited)
            if building:
                return building

    for rel in getattr(ifc_product, "Decomposes", []) or []:
        parent = rel.RelatingObject
        if parent.is_a("IfcBuilding"):
            return parent
        if parent:
            building = get_building_recursive(parent, visited)
            if building:
                return building

    for rel in getattr(ifc_product, "ConnectedTo", []) or []:
        parent = rel.RelatingElement
        if parent.is_a("IfcBuilding"):
            return parent
        if parent:
            building = get_building_recursive(parent, visited)
            if building:
                return building

    return None


def get_opening_element(ifc_element):
    fills = ifc_element.FillsVoids
    if not fills:
        return None

    opening = fills[0].RelatingOpeningElement

    voids = opening.VoidsElements
    if not voids:
        return None

    host = voids[0].RelatingBuildingElement
    return host
