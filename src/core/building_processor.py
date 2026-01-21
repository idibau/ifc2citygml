import logging
from collections import defaultdict

import numpy as np

from model.building.building import Building
from model.building.building_constructive_element import BuildingConstructiveElement
from model.building.storey import Storey
from model.filling import Filling
from model.solid import Solid
from utils.geometry import extract_geometry, get_min_max_from_vertices
from utils.ifc_mapper import map_to_building_entity
from utils.ifc_utils import get_building_storey, get_opening_element

logger = logging.getLogger(__name__)


class BuildingProcessor:
    def __init__(self):
        self.envelope_min = None
        self.envelope_max = None

    def process(self, ifc_building_products, config, document):
        logger.info(f"Processing {len(ifc_building_products)} building product elements...")

        ifc_buildings_by_id = {}
        ifc_products_by_building_id = defaultdict(list)

        for ifc_product, ifc_building in ifc_building_products:
            building_id = getattr(ifc_building, "GlobalId")
            if building_id not in ifc_buildings_by_id:
                ifc_buildings_by_id[building_id] = ifc_building
            ifc_products_by_building_id[building_id].append(ifc_product)

        number_of_buildings = len(ifc_buildings_by_id)
        for building_index, (building_id, ifc_building) in enumerate(ifc_buildings_by_id.items()):
            logger.debug(f"Processing {building_index + 1}/{number_of_buildings} building element...")

            storeys_by_id = {}
            features_by_id = {}
            filling_opening_mapping_by_id = defaultdict(list)

            building = Building(ifc_building)

            number_of_building_products = len(ifc_products_by_building_id[building_id])
            for index, ifc_product in enumerate(ifc_products_by_building_id[building_id]):
                feature_id = getattr(ifc_product, "GlobalId")
                logger.debug(
                    f"Processing {index + 1}/{number_of_building_products} building product element with id {feature_id}")

                if not getattr(ifc_product, "Representation", None):
                    continue

                feature = map_to_building_entity(ifc_product, config)
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
                    ifc_storey = get_building_storey(ifc_product)
                    if ifc_storey:
                        storey_id = getattr(ifc_storey, "GlobalId")
                        if storey_id not in storeys_by_id:
                            storeys_by_id[storey_id] = Storey(ifc_storey)
                            building.add_storey(storeys_by_id[storey_id])
                        storey = storeys_by_id[storey_id]
                        storey.add_building_feature(feature)
                    else:
                        building.add_building_feature(feature)

            for open_id, fill_id in filling_opening_mapping_by_id.items():
                filling = features_by_id.get(fill_id)
                opening = features_by_id.get(open_id)
                if isinstance(filling, Filling) and isinstance(opening, BuildingConstructiveElement):
                    opening.add_filling(filling)

            document.add_building(building)

    def _update_envelope(self, vertices):
        product_min, product_max = get_min_max_from_vertices(vertices)
        if self.envelope_min is None:
            self.envelope_min = product_min
            self.envelope_max = product_max
        else:
            self.envelope_min = np.minimum(self.envelope_min, product_min)
            self.envelope_max = np.maximum(self.envelope_max, product_max)
