from utils.gml_utils import create_element


class BaseFeature:

    def __init__(self, namespace, tag):
        self.element = create_element(namespace, tag)