from ifc2gml.gml.building_constructive_element import BuildingConstructiveElement
from ifc2gml.gml.door import Door
from ifc2gml.gml.window import Window


def map_ifc_entity_to_building_construction_element(ifc_type, predefined_type=None):
    building_construction_element_mapping = {
        "IfcBeam": "beam",
        "IfcBuildingElementComponent": "component",
        "IfcBuildingElementProxy": "proxy",
        "IfcColumn": "column",
        "IfcPile": "pile",
        "IfcRailing": "railing",
        "IfcRamp": "ramp",
        "IfcRampFlight": "rampFlight",
        "IfcStair": "stair",
        "IfcStairFlight": "stairFlight",
        "IfcCurtainWall": "curtainWall",
        "IfcFooting": "footing",
        "IfcMember": "member",
        "IfcPlate": "plate",
        "IfcWall": "wall",
        "IfcWallStandardCase": "wall",
        "IfcRoof": "roof",
        "IfcSpace": "space",
        "IfcCovering": "covering",
        "IfcSlab": "slab"
    }
    if ifc_type in building_construction_element_mapping:
        class_value = building_construction_element_mapping[ifc_type]
        return BuildingConstructiveElement(class_value)

    if ifc_type == "IfcDoor":
        return Door()
    if ifc_type == "IfcWindow":
        return Window()

    return None


from ifc2gml.gml.building_installation import BuildingInstallation
from ifc2gml.gml.closure_surface import ClosureSurface
from ifc2gml.gml.door_surface import DoorSurface
from ifc2gml.gml.roof_surface import RoofSurface
from ifc2gml.gml.wall_surface import WallSurface
from ifc2gml.gml.window_surface import WindowSurface


def map_ifc_entity_to_surface(ifc_type, predefined_type=None):
    if ifc_type in ["IfcBeam",
                    "IfcBuildingElementComponent",
                    "IfcBuildingElementProxy",
                    "IfcColumn",
                    "IfcPile",
                    "IfcRailing",
                    "IfcRamp",
                    "IfcRampFlight",
                    "IfcStair",
                    "IfcStairFlight"]:
        return BuildingInstallation()
    elif ifc_type in ["IfcCurtainWall",
                      "IfcFooting",
                      "IfcMember",
                      "IfcPlate",
                      "IfcWall",
                      "IfcWallStandardCase"]:
        return WallSurface()
    elif ifc_type == "IfcDoor":
        return DoorSurface()
    elif ifc_type == "IfcWindow":
        return WindowSurface()
    elif ifc_type == "IfcRoof":
        return RoofSurface()
    elif ifc_type == "IfcSpace":
        return ClosureSurface()
    elif ifc_type == "IfcCovering":
        if predefined_type == "ROOFING":
            return RoofSurface()
        else:
            return WallSurface()
    elif ifc_type == "IfcSlab":
        if predefined_type == "FLOOR":
            return WallSurface()
        elif predefined_type == "ROOF":
            return RoofSurface()
        elif predefined_type == "LANDING":
            return BuildingInstallation()
        elif predefined_type == "BASESLAB":
            return WallSurface()
        elif predefined_type == "USERDEFINED":
            return WallSurface()
        else:
            return WallSurface()
    return None
