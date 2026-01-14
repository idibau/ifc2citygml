import logging
from collections import defaultdict

from model.building.building import Building
from model.building.building_constructive_element import BuildingConstructiveElement
from model.building.storey import Storey
from model.filling import Filling
from model.solid import Solid
from utils.geometry import extract_geometry
from utils.ifc_mapper import map_ifc_building_entity
from utils.ifc_utils import get_building_storey, get_opening_element

logger = logging.getLogger(__name__)


class BuildingProcessor:
    def __init__(self):
        self.features_by_storey_gid = defaultdict(list)
        self.storey_gids_by_building_gid = defaultdict(set)
        self.features_by_building_gid = defaultdict(list)
        self.buildings_and_storeys_by_gid = {}
        self.filling_gids_by_opening_gids = {}
        self.features_by_gid = {}
        self.envelope_points = []

    def process(self, building_products, config):
        logger.debug(f"Processing {len(building_products)} Building elements...")

        for ifc_product, building in building_products:
            if not getattr(ifc_product, "Representation", None):
                continue

            gid = getattr(ifc_product, "GlobalId")
            feature = map_ifc_building_entity(ifc_product, config)
            if not feature:
                continue

            geo_data = extract_geometry(ifc_product)
            if not geo_data:
                continue
            faces, vertices = geo_data
            self.envelope_points.append(vertices.reshape(-1, 3))

            feature.set_solid(Solid(config.lod, vertices, faces))
            self.features_by_gid[gid] = feature

            building_gid = getattr(building, "GlobalId")
            self.buildings_and_storeys_by_gid[building_gid] = building

            if isinstance(feature, Filling):
                self._handle_filling(ifc_product, gid)
            else:
                self._handle_structure(ifc_product, feature, building_gid)

        self._connect_fillings()

    def _handle_structure(self, ifc_product, feature, building_gid):
        storey = get_building_storey(ifc_product)
        if storey:
            storey_gid = getattr(storey, "GlobalId")
            self.buildings_and_storeys_by_gid[storey_gid] = storey
            self.storey_gids_by_building_gid[building_gid].add(storey_gid)
            self.features_by_storey_gid[storey_gid].append(feature)
        else:
            self.features_by_building_gid[building_gid].append(feature)

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
            if isinstance(filling, Filling) and isinstance(opening, BuildingConstructiveElement):
                opening.add_filling(filling)

    def add_to_document(self, document):
        for key in self.features_by_building_gid.keys() | self.storey_gids_by_building_gid.keys():
            building_features = self.features_by_building_gid.get(key, [])
            storeys = []
            for storey_id in self.storey_gids_by_building_gid.get(key, []):
                storey_features = self.features_by_storey_gid[storey_id]
                storey = Storey(self.buildings_and_storeys_by_gid[storey_id])
                for storey_feature in storey_features:
                    storey.add_building_feature(storey_feature)
                storeys.append(storey)
            building = Building(self.buildings_and_storeys_by_gid[key])
            for storey in storeys:
                building.add_storey(storey)
            for building_feature in building_features:
                building.add_building_feature(building_feature)
            document.add_building(building)
