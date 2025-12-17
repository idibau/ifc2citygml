from model.base_feature import BaseFeature


class BridgeFurniture(BaseFeature):
    def __init__(self, ifc_entity, predefined_type):
        super().__init__("brid", "BridgeFurniture")

    def add_solid(self, solid):
        self.element.append(solid.element)
