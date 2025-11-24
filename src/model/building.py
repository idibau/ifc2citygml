import logging

from model.base_feature import BaseFeature
from model.building_constructive_element import BuildingConstructiveElement
from model.building_furniture import BuildingFurniture
from model.building_installation import BuildingInstallation
from model.building_room import BuildingRoom
from utils.gml_utils import create_sub_element

logger = logging.getLogger(__name__)


class Building(BaseFeature):
    def __init__(self):
        super().__init__("bldg", "Building")

    def add_storey(self, storey):
        parent = create_sub_element(self.element, "bldg", "buildingSubdivision")
        parent.append(storey.element)

    def add_building_feature(self, base_feature):
        if isinstance(base_feature, BuildingConstructiveElement):
            self.add_building_constructive_element(base_feature)
        elif isinstance(base_feature, BuildingInstallation):
            self.add_building_installation(base_feature)
        elif isinstance(base_feature, BuildingRoom):
            self.add_building_room(base_feature)
        elif isinstance(base_feature, BuildingFurniture):
            self.add_building_furniture(base_feature)
        else:
            logger.warning(f"Could not add building feature of type {type(base_feature).__name__} to building.")

    def add_building_constructive_element(self, building_constructive_element):
        parent = create_sub_element(self.element, "bldg", "buildingConstructiveElement")
        parent.append(building_constructive_element.element)

    def add_building_installation(self, building_installation):
        parent = create_sub_element(self.element, "bldg", "buildingInstallation")
        parent.append(building_installation.element)

    def add_building_room(self, building_room):
        parent = create_sub_element(self.element, "bldg", "buildingRoom")
        parent.append(building_room.element)

    def add_building_furniture(self, building_furniture):
        parent = create_sub_element(self.element, "bldg", "buildingFurniture")
        parent.append(building_furniture.element)
