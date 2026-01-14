import logging

from model.base_feature import BaseFeature
from utils.gml_utils import create_sub_element, create_class_value
from utils.ifc_utils import get_name, get_description

logger = logging.getLogger(__name__)


class CityObject(BaseFeature):

    def __init__(self, namespace, tag, ifc_element):
        super().__init__(namespace, tag)
        self.ifc_element = ifc_element
        self._set_class(create_class_value(ifc_element))
        self.add_name(get_name(ifc_element))
        self._set_description(get_description(ifc_element))
        self.solid = None

    def set_solid(self, solid):
        if not self.solid:
            self.solid = solid
            self.element.append(solid.element)
        else:
            logger.warning(
                f"Solid already exists on city object of ifc element {getattr(self.ifc_element, "GlobalId", None)}")

    def _set_class(self, value):
        class_element = create_sub_element(self.element, "bldg", "class")
        class_element.text = value

    def add_function(self, value):
        function_element = create_sub_element(self.element, "bldg", "function")
        function_element.text = value

    def add_usage(self, value):
        usage_element = create_sub_element(self.element, "bldg", "usage")
        usage_element.text = value

    def add_name(self, name):
        name_element = create_sub_element(self.element, "gml", "name")
        name_element.text = name

    def _set_description(self, description):
        description_element = create_sub_element(self.element, "gml", "description")
        description_element.text = description

    def add_generic_attribute(self, generic_attribute):
        sub_element = create_sub_element(self.element, "core", "genericAttribute")
        sub_element.append(generic_attribute.element)
