import ifcopenshell.geom
import logging
import numpy as np
from ifcopenshell.util.shape import get_faces, get_vertices

from model.building_constructive_element import BuildingConstructiveElement
from model.document import Document
from model.filling import Filling
from model.lod import Lod
from model.solid import Solid
from model.storey import Storey
from utils.ifc_mapper import map_ifc_entity
from utils.ifc_utils import get_opening_element, get_building, get_building_storey
from utils.transformation_matrix import TransformationMatrix

logger = logging.getLogger(__name__)

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)


def convert(model, name, center_model=False):
    features_by_storey = {}
    storeys_by_building = {}
    features_by_building = {}
    features_by_gid = {}
    fillings_to_openings = {}

    logger.debug("Calculate envelope")

    ifc_products = model.by_type("IfcProduct")
    shape_by_gid = {}
    all_points = []
    for ifc_product in ifc_products:
        try:
            shape = ifcopenshell.geom.create_shape(settings, ifc_product)
            gid = getattr(ifc_product, "GlobalId")
            shape_by_gid[gid] = shape
            vertices = np.array(shape.geometry.verts, dtype=np.float64)
            vertices = vertices.reshape(-1, 3)
            all_points.append(vertices)
        except Exception:
            pass

    if len(all_points) == 0:
        raise Exception("No geometries found in model")

    all_points = np.vstack(all_points)
    min_corner = all_points.min(axis=0)
    max_corner = all_points.max(axis=0)
    center = (min_corner + max_corner) / 2.0
    logger.debug(f"Model center: {center}")

    logger.debug("Process ifc products")

    for index, ifc_product in enumerate(ifc_products):
        logger.debug(f"Processing {ifc_product.GlobalId} ({index + 1}/{len(ifc_products)})")
        if not getattr(ifc_product, "Representation", None):
            continue

        ifc_entity = ifc_product.is_a()
        predefined_type = getattr(ifc_product, "PredefinedType", None)

        ifc_building = get_building(ifc_product)
        if ifc_building:
            building_gid = getattr(ifc_building, "GlobalId")

            feature = map_ifc_entity(ifc_entity, predefined_type)
            if feature:
                gid = getattr(ifc_product, "GlobalId")
                try:
                    shape = shape_by_gid[gid]
                except Exception as e:
                    logger.warning(f"Failed to create shape for {ifc_product.GlobalId} - {e}")
                    continue
                occ_shape = shape.geometry

                faces = np.array(get_faces(occ_shape), dtype=np.int64)
                relative_vertices = np.array(get_vertices(occ_shape), dtype=np.float64)
                matrix = TransformationMatrix(ifc_product)
                absolute_vertices = matrix.apply_transformation(relative_vertices)

                if center_model:
                    absolute_vertices -= center

                if isinstance(feature, Filling):
                    opening_element = get_opening_element(ifc_product)
                    if opening_element:
                        fillings_to_openings[gid] = getattr(opening_element, "GlobalId")
                    else:
                        logger.warning(f"Could not retrieve opening element {gid}")
                        continue
                else:
                    ifc_storey = get_building_storey(ifc_product)
                    if ifc_storey:
                        storey_gid = getattr(ifc_storey, "GlobalId")
                        if building_gid not in storeys_by_building:
                            storeys_by_building[building_gid] = set()
                        storeys_by_building[building_gid].add(storey_gid)
                        if storey_gid not in features_by_storey:
                            features_by_storey[storey_gid] = []
                        features_by_storey[storey_gid].append(feature)
                    else:
                        if building_gid not in features_by_building:
                            features_by_building[building_gid] = []
                        features_by_building[building_gid].append(feature)

                solid = Solid(Lod.LOD_3, absolute_vertices, faces)
                feature.add_solid(solid)
                features_by_gid[gid] = feature
            else:
                logger.debug(f"No mapping defined for {ifc_entity}")

    for filling_gid, opening_gid in fillings_to_openings.items():
        filling = features_by_gid[filling_gid]
        opening = features_by_gid.get(opening_gid, None)
        if isinstance(filling, Filling) and isinstance(opening, BuildingConstructiveElement):
            opening.add_filling(filling)
        else:
            logger.warning(f"Could not add filling element for opening {opening_gid} and filling {filling_gid}")

    document = Document(name)
    document.add_envelope(min_corner, max_corner)

    for key in features_by_building.keys() | storeys_by_building.keys():
        building_features = features_by_building.get(key, [])
        storeys = []
        for storey_id in storeys_by_building.get(key, []):
            storey_features = features_by_storey[storey_id]
            storey = Storey()
            for storey_feature in storey_features:
                storey.add_building_feature(storey_feature)
            storeys.append(storey)
        document.add_building(storeys, building_features)

    return document
