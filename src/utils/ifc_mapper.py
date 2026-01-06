from datetime import date

from model.bridge.bridge_constructive_element import BridgeConstructiveElement
from model.bridge.bridge_furniture import BridgeFurniture
from model.bridge.bridge_installation import BridgeInstallation
from model.bridge.bridge_room import BridgeRoom
from model.building.building_constructive_element import BuildingConstructiveElement
from model.building.building_furniture import BuildingFurniture
from model.building.building_installation import BuildingInstallation
from model.building.building_room import BuildingRoom
from model.door import Door
from model.generic_attribute import GenericAttributeSet, IntAttribute, DoubleAttribute, DateAttribute, StringAttribute
from model.generic_occupied_space import GenericOccupiedSpace
from model.window import Window
from utils.ifc_utils import get_pset


def _attach_psets(ifc_element, feature, entity_mapping_list, ifc_entity):
    mapping_entry = next((e for e in entity_mapping_list if e.entity == ifc_entity), None)
    if mapping_entry:
        for pset_name in mapping_entry.property_sets:
            pset = get_pset(ifc_element, pset_name)
            generic_attribute_set = map_ifc_pset(pset_name, pset)
            if generic_attribute_set:
                feature.add_generic_attribute(generic_attribute_set)
    return feature


def map_ifc_pset(pset_name, pset):
    attributes = []
    if pset:
        for property_key, property_value in pset.items():
            if isinstance(property_value, int):
                attributes.append(IntAttribute(property_key, property_value))
            elif isinstance(property_value, float):
                attributes.append(DoubleAttribute(property_key, property_value))
            elif isinstance(property_value, date):
                attributes.append(DateAttribute(property_key, property_value))
            else:
                attributes.append(StringAttribute(property_key, str(property_value)))
    if len(attributes) == 0:
        return None
    return GenericAttributeSet(pset_name, attributes)


def map_ifc_building_entity(ifc_element, config):
    mapping = config.building_mapping
    if not mapping:
        return None

    ifc_entity = ifc_element.is_a()
    predefined_type = getattr(ifc_element, "PredefinedType", None)

    if ifc_entity == "IfcDoor":
        return Door(ifc_entity, predefined_type)
    if ifc_entity == "IfcWindow":
        return Window(ifc_entity, predefined_type)

    if ifc_entity in {e.entity for e in mapping.building_room}:
        feature = BuildingRoom(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.building_room, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.building_furniture}:
        feature = BuildingFurniture(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.building_furniture, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.building_constructive_element}:
        feature = BuildingConstructiveElement(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.building_constructive_element, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.building_installation}:
        feature = BuildingInstallation(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.building_installation, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.door}:
        feature = Door(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.door, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.window}:
        feature = Window(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.door, ifc_entity)

    return None


def map_ifc_bridge_entity(ifc_element, config):
    mapping = config.bridge_mapping
    if not mapping:
        return None

    ifc_entity = ifc_element.is_a()
    predefined_type = getattr(ifc_element, "PredefinedType", None)

    if ifc_entity in {e.entity for e in mapping.bridge_room}:
        feature = BridgeRoom(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.bridge_room, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.bridge_furniture}:
        feature = BridgeFurniture(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.bridge_furniture, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.bridge_constructive_element}:
        feature = BridgeConstructiveElement(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.bridge_constructive_element, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.bridge_installation}:
        feature = BridgeInstallation(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.bridge_installation, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.door}:
        feature = Door(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.door, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.window}:
        feature = Window(ifc_entity, predefined_type)
        return _attach_psets(ifc_element, feature, mapping.door, ifc_entity)

    return None

def map_ifc_entity(ifc_element, config):
    mapping = config.generic_mapping
    if not mapping:
        return None

    ifc_entity = ifc_element.is_a()

    if ifc_entity in {e.entity for e in mapping}:
        feature = GenericOccupiedSpace(ifc_entity)
        return _attach_psets(ifc_element, feature, mapping, ifc_entity)

    return None

