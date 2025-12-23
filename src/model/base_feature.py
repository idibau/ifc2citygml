from utils.gml_utils import create_element, create_tag_with_namespace, create_sub_element


class BaseFeature:

    def __init__(self, namespace, tag):
        self.element = create_element(namespace, tag)

    def set_attribute(self, namespace, tag, value):
        self.element.set(create_tag_with_namespace(namespace, tag), value)

    def add_generic_attribute(self, generic_attribute):
        sub_element = create_sub_element(self.element, "core", "genericAttribute")
        sub_element.append(generic_attribute.element)
