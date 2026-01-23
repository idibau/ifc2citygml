import logging
from collections import defaultdict

import numpy as np

from model.bridge.bridge import Bridge
from model.bridge.bridge_constructive_element import BridgeConstructiveElement
from model.bridge.bridge_part import BridgePart
from model.filling import Filling
from model.solid import Solid
from utils.geometry import extract_geometry, get_min_max_from_vertices
from utils.ifc_mapper import map_to_bridge_entity
from utils.ifc_utils import get_bridge_part, get_opening_element

logger = logging.getLogger(__name__)


class BridgeProcessor:
    def __init__(self):
        self.envelope_min = None
        self.envelope_max = None

    def process(self, ifc_bridge_products, config, document):
        logger.info(f"Processing {len(ifc_bridge_products)} bridge product elements...")

        ifc_bridges_by_id = {}
        ifc_products_by_bridge_id = defaultdict(list)

        for ifc_product, ifc_bridge in ifc_bridge_products:
            bridge_id = getattr(ifc_bridge, "GlobalId")
            if bridge_id not in ifc_bridges_by_id:
                ifc_bridges_by_id[bridge_id] = ifc_bridge
            ifc_products_by_bridge_id[bridge_id].append(ifc_product)

        number_of_bridges = len(ifc_bridges_by_id)
        for bridge_index, (bridge_id, ifc_bridge) in enumerate(ifc_bridges_by_id.items()):
            logger.debug(f"Processing {bridge_index + 1}/{number_of_bridges} bridge element")

            bridge_part_by_id = {}
            features_by_id = {}
            filling_opening_mapping_by_id = defaultdict(list)

            bridge = Bridge(ifc_bridge)

            number_of_bridge_products = len(ifc_products_by_bridge_id[bridge_id])
            for index, ifc_product in enumerate(ifc_products_by_bridge_id[bridge_id]):
                feature_id = getattr(ifc_product, "GlobalId")
                logger.debug(
                    f"Processing {index + 1}/{number_of_bridge_products} bridge product element with id {feature_id}")

                if not getattr(ifc_product, "Representation", None):
                    continue

                feature = map_to_bridge_entity(ifc_product, config)
                if not feature:
                    continue
                else:
                    features_by_id[feature_id] = feature

                geometry = extract_geometry(ifc_product)
                if not geometry:
                    continue
                faces, vertices = geometry

                self._update_envelope(vertices)

                feature.set_solid(Solid(config.lod, vertices, faces))

                if isinstance(feature, Filling):
                    opening = get_opening_element(ifc_product)
                    if opening:
                        opening_id = getattr(opening, "GlobalId")
                        filling_opening_mapping_by_id[opening_id].append(feature_id)
                    else:
                        logger.warning(f"Could not retrieve opening for filling {feature_id}")
                else:
                    ifc_bridge_part = get_bridge_part(ifc_product)
                    if ifc_bridge_part:
                        bridge_part_id = getattr(ifc_bridge_part, "GlobalId")
                        if bridge_part_id not in bridge_part_by_id:
                            bridge_part_by_id[bridge_part_id] = BridgePart(ifc_bridge_part)
                            bridge.add_bridge_part(bridge_part_by_id[bridge_part_id])
                        bridge_part = bridge_part_by_id[bridge_part_id]
                        bridge_part.add_bridge_feature(feature)
                    else:
                        bridge.add_bridge_feature(feature)

            for open_id, fill_ids in filling_opening_mapping_by_id.items():
                for fill_id in fill_ids:
                    filling = features_by_id.get(fill_id)
                    opening = features_by_id.get(open_id)
                    if isinstance(filling, Filling) and isinstance(opening, BridgeConstructiveElement):
                        opening.add_filling(filling)

            document.add_bridge(bridge)

    def _update_envelope(self, vertices):
        product_min, product_max = get_min_max_from_vertices(vertices)
        if self.envelope_min is None:
            self.envelope_min = product_min
            self.envelope_max = product_max
        else:
            self.envelope_min = np.minimum(self.envelope_min, product_min)
            self.envelope_max = np.maximum(self.envelope_max, product_max)
