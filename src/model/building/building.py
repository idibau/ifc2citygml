import logging

from model.building.building_constructive_element import BuildingConstructiveElement
from model.building.building_furniture import BuildingFurniture
from model.building.building_installation import BuildingInstallation
from model.building.building_room import BuildingRoom
from model.city_object import CityObject
from utils.gml_utils import create_sub_element

logger = logging.getLogger(__name__)


class Building(CityObject):
    def __init__(self, ifc_element):
        super().__init__("bldg", "Building", ifc_element)

    def add_storey(self, storey):
        parent = create_sub_element(self.element, "bldg", "buildingSubdivision")
        parent.append(storey.element)

    def add_building_feature(self, building_feature):
        if isinstance(building_feature, BuildingConstructiveElement):
            self._add_building_constructive_element(building_feature)
        elif isinstance(building_feature, BuildingInstallation):
            self._add_building_installation(building_feature)
        elif isinstance(building_feature, BuildingRoom):
            self._add_building_room(building_feature)
        elif isinstance(building_feature, BuildingFurniture):
            self._add_building_furniture(building_feature)
        else:
            logger.warning(f"Could not add building feature of type {type(building_feature).__name__} to building.")

    def _add_building_constructive_element(self, building_constructive_element):
        parent = create_sub_element(self.element, "bldg", "buildingConstructiveElement")
        parent.append(building_constructive_element.element)

    def _add_building_installation(self, building_installation):
        parent = create_sub_element(self.element, "bldg", "buildingInstallation")
        parent.append(building_installation.element)

    def _add_building_room(self, building_room):
        parent = create_sub_element(self.element, "bldg", "buildingRoom")
        parent.append(building_room.element)

    def _add_building_furniture(self, building_furniture):
        parent = create_sub_element(self.element, "bldg", "buildingFurniture")
        parent.append(building_furniture.element)
