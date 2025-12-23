from model.bridge.bridge_base_feature import BridgeBaseFeature


class BridgeInstallation(BridgeBaseFeature):
    def __init__(self, ifc_entity, predefined_type):
        super().__init__("brid", "BridgeInstallation")
        self.add_class(ifc_entity)

    def add_solid(self, solid):
        self.element.append(solid.element)
