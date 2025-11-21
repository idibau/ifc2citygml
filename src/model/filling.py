from model.base_feature import BaseFeature


class Filling(BaseFeature):
    def __init__(self, namespace, tag,  ifc_entity, predefined_type):
        super().__init__(namespace, tag)

    def add_solid(self, solid):
        self.element.append(solid.element)
