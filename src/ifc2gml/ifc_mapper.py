from ifc2gml.gml.building_constructive_element import BuildingConstructiveElement
from ifc2gml.gml.building_furniture import BuildingFurniture
from ifc2gml.gml.building_installation import BuildingInstallation
from ifc2gml.gml.building_room import BuildingRoom
from ifc2gml.gml.door import Door
from ifc2gml.gml.window import Window


def map_ifc_entity(ifc_type, predefined_type=None):
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
        "IfcFlowTerminal"
    }

    if ifc_type == "IfcSpace":
        return BuildingRoom(ifc_type, predefined_type)
    if ifc_type == "IfcFurnishingElement":
        return BuildingFurniture(ifc_type, predefined_type)
    if ifc_type == "IfcDoor":
        return Door(ifc_type, predefined_type)
    if ifc_type == "IfcWindow":
        return Window(ifc_type, predefined_type)

    if ifc_type in constructive_mapping:
        return BuildingConstructiveElement(ifc_type, predefined_type)

    if ifc_type in installation_mapping:
        return BuildingInstallation(ifc_type, predefined_type)

    print(f"Not supported ifc type: {ifc_type}.")
    return None
