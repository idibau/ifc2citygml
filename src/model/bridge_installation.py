from model.base_feature import BaseFeature


class BridgeInstallation(BaseFeature):
    def __init__(self, ifc_entity, predefined_type):
        super().__init__("brid", "BridgeInstallation")

    def add_solid(self, solid):
        self.element.append(solid.element)
