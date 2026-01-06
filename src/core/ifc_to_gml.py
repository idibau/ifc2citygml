import logging
import numpy as np
from ifcopenshell.util.shape import get_faces, get_vertices

from configuration.configuration import Configuration
from core.bridge_processor import BridgeProcessor
from core.building_processor import BuildingProcessor
from core.generic_processor import GenericProcessor
from model.document import Document
from utils.ifc_utils import get_building, get_bridge

logger = logging.getLogger(__name__)


def convert(model, name):
    logger.debug("Starting conversion...")

    config = Configuration.load("/workspace/config.yml")

    products_building = []
    products_bridge = []
    products_generic = []

    all_products = model.by_type("IfcProduct")

    for product in all_products:
        building = get_building(product)
        if building:
            products_building.append((product, building))
            continue

        bridge = get_bridge(product)
        if bridge:
            products_bridge.append((product, bridge))
            continue

        products_generic.append(product)

    building_proc = BuildingProcessor()
    bridge_proc = BridgeProcessor()
    generic_prc = GenericProcessor()

    building_proc.process(products_building, config)
    bridge_proc.process(products_bridge, config)
    generic_prc.process(products_generic, config)

    document = Document(name)

    all_points = building_proc.envelope_points + bridge_proc.envelope_points + generic_prc.envelope_points
    if all_points:
        full_cloud = np.vstack(all_points)
        document.add_envelope(full_cloud.min(axis=0), full_cloud.max(axis=0))

    building_proc.add_to_document(document)
    bridge_proc.add_to_document(document)
    generic_prc.add_to_document(document)

    return document
