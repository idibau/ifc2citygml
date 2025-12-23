import logging
from collections import defaultdict

from configuration.configuration import Configuration
from model.bridge.bridge_constructive_element import BridgeConstructiveElement
from model.bridge.bridge_part import BridgePart
from model.filling import Filling
from model.lod import Lod
from model.solid import Solid
from utils.geometry import extract_geometry
from utils.ifc_mapper import map_ifc_bridge_entity
from utils.ifc_utils import get_bridge_part, get_opening_element

logger = logging.getLogger(__name__)


class BridgeProcessor:
    def __init__(self):
        self.features_by_bridge_part = defaultdict(list)
        self.bridge_parts_by_bridge = defaultdict(set)
        self.features_by_bridge = defaultdict(list)
        self.features_by_gid = {}
        self.fillings_to_openings = {}
        self.envelope_points = []

    def process(self, bridge_products):
        logger.debug(f"Processing {len(bridge_products)} Bridge elements...")

        for ifc_product, bridge in bridge_products:
            if not getattr(ifc_product, "Representation", None):
                continue

            gid = getattr(ifc_product, "GlobalId")
            feature = map_ifc_bridge_entity(ifc_product, Configuration.load("/workspace/config.yml"))
            if not feature:
                continue

            geo_data = extract_geometry(ifc_product)
            if not geo_data:
                continue
            faces, vertices = geo_data
            self.envelope_points.append(vertices.reshape(-1, 3))

            feature.add_solid(Solid(Lod.LOD_3, vertices, faces))
            self.features_by_gid[gid] = feature

            bridge_gid = getattr(bridge, "GlobalId")

            if isinstance(feature, Filling):
                self._handle_filling(ifc_product, gid)
            else:
                self._handle_structure(ifc_product, feature, bridge_gid)

        self._connect_fillings()

    def _handle_structure(self, ifc_product, feature, bridge_gid):
        bridge_part = get_bridge_part(ifc_product)
        if bridge_part:
            part_gid = getattr(bridge_part, "GlobalId")
            self.bridge_parts_by_bridge[bridge_gid].add(part_gid)
            self.features_by_bridge_part[part_gid].append(feature)
        else:
            self.features_by_bridge[bridge_gid].append(feature)

    def _handle_filling(self, ifc_product, gid):
        opening = get_opening_element(ifc_product)
        if opening:
            self.fillings_to_openings[gid] = getattr(opening, "GlobalId")
        else:
            logger.warning(f"Could not retrieve opening for filling {gid}")

    def _connect_fillings(self):
        for fill_id, open_id in self.fillings_to_openings.items():
            filling = self.features_by_gid.get(fill_id)
            opening = self.features_by_gid.get(open_id)
            if isinstance(filling, Filling) and isinstance(opening, BridgeConstructiveElement):
                opening.add_filling(filling)

    def add_to_document(self, document):
        for key in self.features_by_bridge.keys() | self.bridge_parts_by_bridge.keys():
            bridge_features = self.features_by_bridge.get(key, [])
            bridge_parts = []
            for bride_part_id in self.bridge_parts_by_bridge.get(key, []):
                bridge_part_features = self.features_by_bridge_part[bride_part_id]
                bridge_part = BridgePart()
                for bridge_part_feature in bridge_part_features:
                    bridge_part.add_bridge_feature(bridge_part_feature)
                bridge_parts.append(bridge_part)
            document.add_bridge(bridge_parts, bridge_features)
