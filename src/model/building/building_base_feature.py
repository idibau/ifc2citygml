from model.base_feature import BaseFeature
from utils.gml_utils import create_sub_element


class BuildingBaseFeature(BaseFeature):

    def __init__(self, namespace, tag):
        super().__init__(namespace, tag)

    def add_class(self, value):
        class_element = create_sub_element(self.element, "bldg", "class")
        class_element.text = value

    def add_function(self, value):
        function_element = create_sub_element(self.element, "bldg", "function")
        function_element.text = value

    def add_usage(self, value):
        usage_element = create_sub_element(self.element, "bldg", "usage")
        usage_element.text = value