import ifcopenshell.geom
import numpy as np
from ifcopenshell.util.shape import get_faces, get_vertices

from model.building_constructive_element import BuildingConstructiveElement
from model.document import Document
from model.filling import Filling
from model.lod import Lod
from model.solid import Solid
from utils.ifc_mapper import map_ifc_entity
from utils.ifc_utils import get_building_recursive, get_opening_element
from utils.transformation_matrix import TransformationMatrix

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)


def convert(model, name):
    buildings_by_global_id = {}
    city_objects_by_global_id = {}
    fillings_to_openings = {}

    center = None

    print("Process ifc products")
    ifc_products = model.by_type("IfcProduct")
    for index, ifc_product in enumerate(ifc_products):
        print(f"Processing {ifc_product.GlobalId} ({index + 1}/{len(ifc_products)})")
        if not getattr(ifc_product, "Representation", None):
            continue

        entity = ifc_product.is_a()
        predefined_type = getattr(ifc_product, "PredefinedType", None)

        ifc_building = get_building_recursive(ifc_product)
        if ifc_building:
            try:
                shape = ifcopenshell.geom.create_shape(settings, ifc_product)
            except Exception as e:
                print(f"Failed to create shape for {ifc_product.GlobalId} - {e}")
                continue
            occ_shape = shape.geometry

            faces = np.array(get_faces(occ_shape), dtype=np.int64)
            relative_vertices = np.array(get_vertices(occ_shape), dtype=np.float64)
            matrix = TransformationMatrix(ifc_product)
            absolute_vertices = matrix.apply_transformation(relative_vertices)

            if center is None:
                center = absolute_vertices.mean(axis=0)
                print(center)

            # absolute_vertices -= center

            base_feature = map_ifc_entity(entity, predefined_type)
            if base_feature:
                global_id = getattr(ifc_product, "GlobalId")
                if isinstance(base_feature, Filling):
                    opening_element = get_opening_element(ifc_product)
                    if opening_element:
                        fillings_to_openings[global_id] = getattr(opening_element, "GlobalId")
                    else:
                        print("Could not retrieve opening element")
                        continue
                else:
                    building_global_id = getattr(ifc_building, "GlobalId")
                    if building_global_id not in buildings_by_global_id:
                        buildings_by_global_id[building_global_id] = []
                    buildings_by_global_id[building_global_id].append(base_feature)

                solid = Solid(Lod.LOD_3, absolute_vertices, faces)
                base_feature.add_solid(solid)
                city_objects_by_global_id[global_id] = base_feature
            else:
                print("Could not retrieve GML entity")

    for filling_gid, opening_gid in fillings_to_openings.items():
        filling = city_objects_by_global_id[filling_gid]
        opening = city_objects_by_global_id.get(opening_gid, None)
        if isinstance(filling, Filling) and isinstance(opening, BuildingConstructiveElement):
            opening.add_filling(filling)
        else:
            print("Could not add filling element")

    document = Document(name)
    for building_features in buildings_by_global_id.values():
        document.add_building(building_features)

    return document
