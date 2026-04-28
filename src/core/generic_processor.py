import logging

import numpy as np

from model.solid import Solid
from utils.geometry import extract_geometry, get_min_max_from_vertices
from utils.ifc_mapper import map_to_generic_feature

logger = logging.getLogger(__name__)


class GenericProcessor:
    def __init__(self):
        self.envelope_min = None
        self.envelope_max = None

    def process(self, ifc_products, config, document):
        number_of_products = len(ifc_products)
        logger.info(f"Processing {number_of_products} generic elements")

        for index, ifc_product in enumerate(ifc_products):
            feature_id = getattr(ifc_product, "GlobalId")
            logger.debug(f"Processing {index + 1}/{number_of_products} generic element with id {feature_id}")

            if not getattr(ifc_product, "Representation", None):
                continue

            feature = map_to_generic_feature(ifc_product, config)
            if not feature:
                continue

            geo_data = extract_geometry(ifc_product)
            if not geo_data:
                continue
            faces, vertices = geo_data

            self._update_envelope(vertices)

            feature.set_solid(Solid(config.lod, vertices, faces))
            document.add_generic(feature)

    def _update_envelope(self, vertices):
        product_min, product_max = get_min_max_from_vertices(vertices)
        if self.envelope_min is None:
            self.envelope_min = product_min
            self.envelope_max = product_max
        else:
            self.envelope_min = np.minimum(self.envelope_min, product_min)
            self.envelope_max = np.maximum(self.envelope_max, product_max)
