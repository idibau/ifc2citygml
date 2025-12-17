import logging
import numpy as np
from ifcopenshell.util.shape import get_faces, get_vertices

from core.bridge_processor import BridgeProcessor
from core.building_processor import BuildingProcessor
from model.document import Document
from utils.ifc_utils import get_building, get_bridge

logger = logging.getLogger(__name__)


def convert(model, name):
    logger.debug("Starting conversion...")

    products_building = []
    products_bridge = []

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

    building_proc = BuildingProcessor()
    bridge_proc = BridgeProcessor()

    building_proc.process(products_building)
    bridge_proc.process(products_bridge)

    document = Document(name)

    all_points = building_proc.envelope_points + bridge_proc.envelope_points
    if all_points:
        full_cloud = np.vstack(all_points)
        document.add_envelope(full_cloud.min(axis=0), full_cloud.max(axis=0))

    building_proc.add_to_document(document)
    bridge_proc.add_to_document(document)

    return document
