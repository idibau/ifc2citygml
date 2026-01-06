import logging

from model.base_feature import BaseFeature
from utils.gml_utils import create_sub_element

logger = logging.getLogger(__name__)


class GenericOccupiedSpace(BaseFeature):
    def __init__(self, ifc_entity):
        super().__init__("gen", "GenericOccupiedSpace")
        self.add_class(ifc_entity)

    def add_solid(self, solid):
        self.element.append(solid.element)

    def add_class(self, value):
        class_element = create_sub_element(self.element, "gen", "class")
        class_element.text = value

    def add_function(self, value):
        function_element = create_sub_element(self.element, "gen", "function")
        function_element.text = value

    def add_usage(self, value):
        usage_element = create_sub_element(self.element, "gen", "usage")
        usage_element.text = value
