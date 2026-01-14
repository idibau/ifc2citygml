import logging

from model.bridge.bridge_constructive_element import BridgeConstructiveElement
from model.bridge.bridge_furniture import BridgeFurniture
from model.bridge.bridge_installation import BridgeInstallation
from model.bridge.bridge_room import BridgeRoom
from model.city_object import CityObject
from utils.gml_utils import create_sub_element

logger = logging.getLogger(__name__)


class BridgePart(CityObject):
    def __init__(self, ifc_element):
        super().__init__("brid", "BridgePart", ifc_element)

    def add_bridge_feature(self, base_feature):
        if isinstance(base_feature, BridgeConstructiveElement):
            self.add_bridge_constructive_element(base_feature)
        elif isinstance(base_feature, BridgeInstallation):
            self.add_bridge_installation(base_feature)
        elif isinstance(base_feature, BridgeRoom):
            self.add_bridge_room(base_feature)
        elif isinstance(base_feature, BridgeFurniture):
            self.add_bridge_furniture(base_feature)
        else:
            logger.warning(f"Could not add bridge feature of type {type(base_feature).__name__} to bridge.")

    def add_bridge_constructive_element(self, bridge_constructive_element):
        parent = create_sub_element(self.element, "brid", "bridgeConstructiveElement")
        parent.append(bridge_constructive_element.element)

    def add_bridge_installation(self, bridge_installation):
        parent = create_sub_element(self.element, "brid", "bridgeInstallation")
        parent.append(bridge_installation.element)

    def add_bridge_room(self, bridge_room):
        parent = create_sub_element(self.element, "brid", "bridgeRoom")
        parent.append(bridge_room.element)

    def add_bridge_furniture(self, bridge_furniture):
        parent = create_sub_element(self.element, "brid", "bridgeFurniture")
        parent.append(bridge_furniture.element)
