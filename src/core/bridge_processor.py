import logging
from collections import defaultdict

from model.bridge.bridge import Bridge
from model.bridge.bridge_constructive_element import BridgeConstructiveElement
from model.bridge.bridge_part import BridgePart
from model.filling import Filling
from model.solid import Solid
from utils.geometry import extract_geometry
from utils.ifc_mapper import map_ifc_bridge_entity
from utils.ifc_utils import get_bridge_part, get_opening_element

logger = logging.getLogger(__name__)


class BridgeProcessor:
    def __init__(self):
        self.features_by_bridge_part_gid = defaultdict(list)
        self.bridge_part_gids_by_bridge_gid = defaultdict(set)
        self.features_by_bridge_gid = defaultdict(list)
        self.bridges_and_parts_by_gid = {}
        self.filling_gids_by_opening_gids = {}
        self.features_by_gid = {}
        self.envelope_points = []

    def process(self, bridge_products, config):
        logger.debug(f"Processing {len(bridge_products)} Bridge elements...")

        for ifc_product, bridge in bridge_products:
            if not getattr(ifc_product, "Representation", None):
                continue

            gid = getattr(ifc_product, "GlobalId")
            feature = map_ifc_bridge_entity(ifc_product, config)
            if not feature:
                continue

            geo_data = extract_geometry(ifc_product)
            if not geo_data:
                continue
            faces, vertices = geo_data
            self.envelope_points.append(vertices.reshape(-1, 3))

            feature.set_solid(Solid(config.lod, vertices, faces))
            self.features_by_gid[gid] = feature

            bridge_gid = getattr(bridge, "GlobalId")
            self.bridges_and_parts_by_gid[bridge_gid] = bridge

            if isinstance(feature, Filling):
                self._handle_filling(ifc_product, gid)
            else:
                self._handle_structure(ifc_product, feature, bridge_gid)

        self._connect_fillings()

    def _handle_structure(self, ifc_product, feature, bridge_gid):
        bridge_part = get_bridge_part(ifc_product)
        if bridge_part:
            part_gid = getattr(bridge_part, "GlobalId")
            self.bridges_and_parts_by_gid[part_gid] = bridge_part
            self.bridge_part_gids_by_bridge_gid[bridge_gid].add(part_gid)
            self.features_by_bridge_part_gid[part_gid].append(feature)
        else:
            self.features_by_bridge_gid[bridge_gid].append(feature)

    def _handle_filling(self, ifc_product, gid):
        opening = get_opening_element(ifc_product)
        if opening:
            self.filling_gids_by_opening_gids[gid] = getattr(opening, "GlobalId")
        else:
            logger.warning(f"Could not retrieve opening for filling {gid}")

    def _connect_fillings(self):
        for fill_id, open_id in self.filling_gids_by_opening_gids.items():
            filling = self.features_by_gid.get(fill_id)
            opening = self.features_by_gid.get(open_id)
            if isinstance(filling, Filling) and isinstance(opening, BridgeConstructiveElement):
                opening.add_filling(filling)

    def add_to_document(self, document):
        for key in self.features_by_bridge_gid.keys() | self.bridge_part_gids_by_bridge_gid.keys():
            bridge_features = self.features_by_bridge_gid.get(key, [])
            bridge_parts = []
            for bride_part_id in self.bridge_part_gids_by_bridge_gid.get(key, []):
                bridge_part_features = self.features_by_bridge_part_gid[bride_part_id]
                bridge_part = BridgePart(self.bridges_and_parts_by_gid[bride_part_id])
                for bridge_part_feature in bridge_part_features:
                    bridge_part.add_bridge_feature(bridge_part_feature)
                bridge_parts.append(bridge_part)
            bridge = Bridge(self.bridges_and_parts_by_gid[key])
            for bridge_part in bridge_parts:
                bridge.add_bridge_part(bridge_part)
            for bridge_feature in bridge_features:
                bridge.add_bridge_feature(bridge_feature)
            document.add_bridge(bridge)

