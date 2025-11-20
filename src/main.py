import ifcopenshell.geom
from ifcopenshell.util.shape import get_faces, get_vertices
import numpy as np
import ifcopenshell

from utils.ifc_utils import get_building_recursive
from utils.transformation_matrix import TransformationMatrix


# Geometry settings
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_WORLD_COORDS, True)

# Load IFC and get a product
model = ifcopenshell.open("/workspace/src/model_with_origin_50.ifc")


product = model.by_type("IfcWall")[0]

building = get_building_recursive(product)

# Generate the geometry
shape = ifcopenshell.geom.create_shape(settings, product)
occ_shape = shape.geometry

# Extract raw vertices and faces
vertices = np.array(get_vertices(occ_shape))
faces = np.array(get_faces(occ_shape))

matrix = TransformationMatrix(product)

verts_world = matrix.apply_transformation(vertices)

print("Vertices (world coordinates):")
print(verts_world[:5])
print("Faces:", faces.shape)
