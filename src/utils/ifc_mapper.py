from model.building_constructive_element import BuildingConstructiveElement
from model.building_furniture import BuildingFurniture
from model.building_installation import BuildingInstallation
from model.building_room import BuildingRoom
from model.bridge_constructive_element import BridgeConstructiveElement
from model.bridge_furniture import BridgeFurniture
from model.bridge_installation import BridgeInstallation
from model.bridge_room import BridgeRoom
from model.door import Door
from model.window import Window


def map_ifc_building_entity(ifc_type, predefined_type=None):
    constructive_mapping = [
        "IfcBeam",
        "IfcColumn",
        "IfcFooting",
        "IfcMember",
        "IfcPlate",
        "IfcWall",
        "IfcWallStandardCase",
        "IfcRoof",
        "IfcCurtainWall",
        "IfcSlab",
        "IfcCovering"
    ]

    installation_mapping = {
        "IfcRailing",
        "IfcRamp",
        "IfcRampFlight",
        "IfcStair",
        "IfcStairFlight",
        "IfcBuildingElementProxy",
        "IfcBuildingElementComponent",
        "IfcPile",
        # "IfcFlowTerminal"
    }

    if ifc_type == "IfcSpace":
        return BuildingRoom(ifc_type, predefined_type)
    # if ifc_type == "IfcFurnishingElement":
    #     return BuildingFurniture(ifc_type, predefined_type)
    if ifc_type == "IfcDoor":
        return Door(ifc_type, predefined_type)
    if ifc_type == "IfcWindow":
        return Window(ifc_type, predefined_type)

    if ifc_type in constructive_mapping:
        return BuildingConstructiveElement(ifc_type, predefined_type)

    if ifc_type in installation_mapping:
        return BuildingInstallation(ifc_type, predefined_type)
    return None


def map_ifc_bridge_entity(ifc_type, predefined_type=None):
    constructive_mapping = [
        "IfcBeam",
        "IfcColumn",
        "IfcFooting",
        "IfcMember",
        "IfcPlate",
        "IfcWall",
        "IfcWallStandardCase",
        "IfcRoof",
        "IfcCurtainWall",
        "IfcSlab",
        "IfcCovering"
    ]

    installation_mapping = {
        "IfcRailing",
        "IfcRamp",
        "IfcRampFlight",
        "IfcStair",
        "IfcStairFlight",
        "IfcBuildingElementProxy",
        "IfcBuildingElementComponent",
        "IfcPile",
        # "IfcFlowTerminal"
    }

    if ifc_type == "IfcSpace":
        return BridgeRoom(ifc_type, predefined_type)
    # if ifc_type == "IfcFurnishingElement":
    #     return BuildingFurniture(ifc_type, predefined_type)
    if ifc_type == "IfcDoor":
        return Door(ifc_type, predefined_type)
    if ifc_type == "IfcWindow":
        return Window(ifc_type, predefined_type)

    if ifc_type in constructive_mapping:
        return BridgeConstructiveElement(ifc_type, predefined_type)

    if ifc_type in installation_mapping:
        return BridgeInstallation(ifc_type, predefined_type)
    return None
