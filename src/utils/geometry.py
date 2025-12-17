import logging
import numpy as np
import ifcopenshell.geom
from ifcopenshell.util.shape import get_faces, get_vertices
from utils.transformation_matrix import TransformationMatrix

logger = logging.getLogger(__name__)

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)


def extract_geometry(ifc_product):
    try:
        shape = ifcopenshell.geom.create_shape(settings, ifc_product)
    except Exception as e:
        logger.warning(f"Failed to create shape for {ifc_product.GlobalId} - {e}")
        return None

    occ_shape = shape.geometry
    faces = np.array(get_faces(occ_shape), dtype=np.int64)
    relative_vertices = np.array(get_vertices(occ_shape), dtype=np.float64)

    matrix = TransformationMatrix(ifc_product)
    absolute_vertices = matrix.apply_transformation(relative_vertices)
    return faces, absolute_vertices