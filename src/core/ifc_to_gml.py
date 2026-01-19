import logging
import numpy as np

from core.bridge_processor import BridgeProcessor
from core.building_processor import BuildingProcessor
from core.generic_processor import GenericProcessor
from utils.geometry import get_min_max_from_vertices
from utils.ifc_utils import get_building, get_bridge

logger = logging.getLogger(__name__)


def convert(model, document, config):
    logger.debug("Starting conversion...")

    products_building = []
    products_bridge = []
    products_generic = []

    all_products = model.by_type("IfcProduct")

    for product in all_products:

        if config.building_mapping:
            building = get_building(product)
            if building:
                products_building.append((product, building))
                continue

        if config.bridge_mapping:
            bridge = get_bridge(product)
            if bridge:
                products_bridge.append((product, bridge))
                continue

        if config.generic_mapping and self.is_generic_mapped_product(product):
            products_generic.append(product)

    building_proc = BuildingProcessor()
    bridge_proc = BridgeProcessor()
    generic_prc = GenericProcessor()

    building_proc.process(products_building, config, document)
    bridge_proc.process(products_bridge, config, document)
    generic_prc.process(products_generic, config, document)

    envelope_points = np.array([point for point in
                                [building_proc.envelope_max, bridge_proc.envelope_max, generic_prc.envelope_max,
                                 building_proc.envelope_min, bridge_proc.envelope_min, generic_prc.envelope_min] if
                                point is not None])
    min_point, max_point = get_min_max_from_vertices(envelope_points)
    if min_point is not None and max_point is not None:
        document.add_envelope(min_point, max_point)

    return document


def is_generic_mapped_product(ifc_product, config):
    entity = ifc_product.is_a()
    return entity in [entity_mapping.entity for entity_mapping in config.generic_mapping]
