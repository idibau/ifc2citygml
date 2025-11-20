import numpy as np

import math
import ifcopenshell.util.placement as placement_util

from utils.ifc_utils import get_absolute_placement, get_spatial_parent


class TransformationMatrix:

    def __init__(self, ifc_product):
        self.m = np.eye(4)
        self.add_object_placement_transformation(ifc_product)
        self.add_context_transformation(ifc_product)
        self.add_map_conversion_transformation(ifc_product)

    @property
    def translation(self):
        return self.m[:3, 3]

    @property
    def rotation(self):
        return self.m[:3, :3]

    def apply_transformation(self, vertices):
        return (vertices @ self.rotation.T) + self.translation

    def add_transformation(self, m):
        self.m = self.m @ m

    def add_context_transformation(self, ifc_product):
        representation = getattr(ifc_product, "Representation", None)
        if not representation or not representation.Representations:
            return
        context = representation.Representations[0].ContextOfItems
        if context.is_a("IfcGeometricRepresentationSubContext"):
            context = context.ParentContext
        wcs = getattr(context, "WorldCoordinateSystem", None)
        if wcs:
            self.add_transformation(placement_util.get_axis2placement(wcs))

    def add_map_conversion_transformation(self, ifc_product):
        representation = getattr(ifc_product, "Representation", None)
        if not representation or not representation.Representations:
            return
        context = representation.Representations[0].ContextOfItems
        if context.is_a("IfcGeometricRepresentationSubContext"):
            context = context.ParentContext
        if hasattr(context, "HasCoordinateOperation") and context.HasCoordinateOperation:
            map_conversion = context.HasCoordinateOperation[0]
            east = map_conversion.Eastings or 0.0
            north = map_conversion.Northings or 0.0
            height = map_conversion.OrthogonalHeight or 0.0
            x_abs = map_conversion.XAxisAbscissa
            x_ord = map_conversion.XAxisOrdinate
            scale = map_conversion.Scale or 1.0

            rot = math.atan2(x_ord, x_abs)

            m = np.eye(4)
            m[:3, :3] = np.array([
                [math.cos(rot), -math.sin(rot), 0.0],
                [math.sin(rot), math.cos(rot), 0.0],
                [0.0, 0.0, 1.0]
            ]) * scale
            m[:3, 3] = np.array([east, north, height])
            self.add_transformation(m)

    def add_object_placement_transformation(self, ifc_product):
        """Combine placement chain: product + all spatial parents."""
        placement = getattr(ifc_product, "ObjectPlacement", None)
        m = get_absolute_placement(placement) if placement else np.eye(4)
        parent = get_spatial_parent(ifc_product)
        while parent:
            parent_place = getattr(parent, "ObjectPlacement", None)
            if parent_place:
                m = get_absolute_placement(parent_place) @ m
            parent = get_spatial_parent(parent)
        return m