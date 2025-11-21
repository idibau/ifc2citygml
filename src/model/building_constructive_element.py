from model.base_feature import BaseFeature
from utils.gml_utils import create_sub_element

class BuildingConstructiveElement(BaseFeature):
    def __init__(self, ifc_entity, predefined_type):
        super().__init__("bldg", "BuildingConstructiveElement")

    def add_solid(self, solid):
        self.element.append(solid.element)

    def add_filling(self, filling):
        parent = create_sub_element(self.element, "con", "filling")
        parent.append(filling.element)
