import ifcopenshell.geom
import numpy as np
from ifcopenshell.util.shape import get_faces, get_vertices

from ifc2gml.gml.building_constructive_element import BuildingConstructiveElement
from ifc2gml.gml.document import Document
from ifc2gml.gml.filling import Filling
from ifc2gml.gml.filling_surface import FillingSurface
from ifc2gml.gml.lod import Lod
from ifc2gml.gml.surface import Surface
from ifc2gml.ifc_to_gml_mapper import map_ifc_entity_to_surface
from utils.ifc_utils import get_building_recursive, get_opening_element
from utils.transformation_matrix import TransformationMatrix

settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

print("Reading file")


def run(file_name):
    model = ifcopenshell.open(f"/workspace/input/{file_name}.ifc")

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

            city_object = map_ifc_entity_to_surface(entity, predefined_type)
            if city_object:
                global_id = getattr(ifc_product, "GlobalId")
                if isinstance(city_object, Filling) or isinstance(city_object, FillingSurface):
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
                    buildings_by_global_id[building_global_id].append(city_object)

                city_object.add_multi_surface(absolute_vertices, faces, Lod.LOD_3)
                city_objects_by_global_id[global_id] = city_object
            else:
                print("Could not retrieve GML entity")

    for filling_gid, opening_gid in fillings_to_openings.items():
        filling = city_objects_by_global_id[filling_gid]
        opening = city_objects_by_global_id.get(opening_gid, None)
        if isinstance(filling, Filling) and isinstance(opening, BuildingConstructiveElement):
            opening.add_filling(filling)
        elif isinstance(filling, FillingSurface) and isinstance(opening, Surface):
            opening.add_filling_surface(filling)
        else:
            print("Could not add filling element")

    gml_document = Document("Test")
    for gml_elements in buildings_by_global_id.values():
        gml_document.add_city_object_member(gml_elements)

    gml_document.write(f"/workspace/output/ifc2gml_surface_non_centered_{file_name}.gml")


# for file in os.listdir("/workspace/input"):
#     file_name = file.replace(".ifc", "")
#     run(file_name)

run("0114-B+P-AR-HAUS_A-M3-01")

print("done")
