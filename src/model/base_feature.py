from utils.gml_utils import get_uuid_as_string, create_element, create_tag_with_namespace


class BaseFeature:

    def __init__(self, namespace, tag):
        self.element = create_element(namespace, tag)

    def set_id(self):
        self.element.set(create_tag_with_namespace("gml", "id"), get_uuid_as_string())
