from collections import defaultdict
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
from model.other_construction import OtherConstruction
from model.window import Window
from utils.ifc_utils import get_pset


def _attach_psets_and_attributes(ifc_element, feature, entity_mapping_list, ifc_entity):
    mapping_entry = next((e for e in entity_mapping_list if e.entity == ifc_entity), None)
    if mapping_entry:
        properties_by_psets = defaultdict(list)
        for item in mapping_entry.properties:
            pset, property_name = item.split(".", 1)
            properties_by_psets[pset].append(property_name)

        for pset_name, property_names in properties_by_psets.items():
            pset = get_pset(ifc_element, pset_name)
            if pset is not None:
                filtered_pset = {}
                for property_name in property_names:
                    if property_name in pset:
                        filtered_pset[property_name] = pset[property_name]
                generic_attribute_set = _map_ifc_pset(pset_name, filtered_pset)
                if generic_attribute_set:
                    feature.add_generic_attribute(generic_attribute_set)

        for item in mapping_entry.attributes:
            attribute = getattr(ifc_element, item, None)
            if attribute is not None:
                feature.add_generic_attribute(_create_generic_attribute(item, attribute))

    return feature


def _map_ifc_pset(pset_name, pset):
    attributes = []
    if pset:
        for property_key, property_value in pset.items():
            attributes.append(_create_generic_attribute(property_key, property_value))
    if len(attributes) == 0:
        return None
    return GenericAttributeSet(pset_name, attributes)


def _create_generic_attribute(key, value):
    if not isinstance(value, bool) and isinstance(value, int):
        return IntAttribute(key, value)
    elif isinstance(value, float):
        return DoubleAttribute(key, value)
    elif isinstance(value, date):
        return DateAttribute(key, value)
    else:
        return StringAttribute(key, str(value))


def map_to_building_entity(ifc_element, config):
    mapping = config.building_mapping
    if not mapping:
        return None

    ifc_entity = ifc_element.is_a()

    if ifc_entity in {e.entity for e in mapping.building_room}:
        feature = BuildingRoom(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.building_room, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.building_furniture}:
        feature = BuildingFurniture(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.building_furniture, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.building_constructive_element}:
        feature = BuildingConstructiveElement(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.building_constructive_element, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.building_installation}:
        feature = BuildingInstallation(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.building_installation, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.door}:
        feature = Door(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.door, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.window}:
        feature = Window(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.door, ifc_entity)

    return None


def map_to_bridge_entity(ifc_element, config):
    mapping = config.bridge_mapping
    if not mapping:
        return None

    ifc_entity = ifc_element.is_a()

    if ifc_entity in {e.entity for e in mapping.bridge_room}:
        feature = BridgeRoom(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.bridge_room, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.bridge_furniture}:
        feature = BridgeFurniture(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.bridge_furniture, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.bridge_constructive_element}:
        feature = BridgeConstructiveElement(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.bridge_constructive_element, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.bridge_installation}:
        feature = BridgeInstallation(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.bridge_installation, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.door}:
        feature = Door(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.door, ifc_entity)

    if ifc_entity in {e.entity for e in mapping.window}:
        feature = Window(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping.door, ifc_entity)

    return None


def map_to_other_construction_entity(ifc_element, config):
    mapping = config.other_construction_mapping
    if not mapping:
        return None

    ifc_entity = ifc_element.is_a()

    if ifc_entity in {e.entity for e in mapping}:
        feature = OtherConstruction(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping, ifc_entity)

    return None


def map_to_generic_entity(ifc_element, config):
    mapping = config.generic_mapping
    if not mapping:
        return None

    ifc_entity = ifc_element.is_a()

    if ifc_entity in {e.entity for e in mapping}:
        feature = GenericOccupiedSpace(ifc_element)
        return _attach_psets_and_attributes(ifc_element, feature, mapping, ifc_entity)

    return None
