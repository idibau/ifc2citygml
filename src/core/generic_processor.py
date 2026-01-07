import logging

from model.solid import Solid
from utils.geometry import extract_geometry
from utils.ifc_mapper import map_ifc_entity

logger = logging.getLogger(__name__)


class GenericProcessor:
    def __init__(self):
        self.features = []
        self.envelope_points = []

    def process(self, products, config):
        logger.debug(f"Processing {len(products)} generic elements...")

        for ifc_product in products:
            if not getattr(ifc_product, "Representation", None):
                continue

            feature = map_ifc_entity(ifc_product, config)
            if not feature:
                continue

            geo_data = extract_geometry(ifc_product)
            if not geo_data:
                continue
            faces, vertices = geo_data
            self.envelope_points.append(vertices.reshape(-1, 3))

            feature.add_solid(Solid(config.lod, vertices, faces))
            self.features.append(feature)

    def add_to_document(self, document):
        for feature in self.features:
            document.add_generic(feature)
