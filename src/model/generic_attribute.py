from model.base_feature import BaseFeature
from utils.gml_utils import create_sub_element


class GenericAttributeSet(BaseFeature):
    def __init__(self, name, attributes):
        super().__init__("gen", "GenericAttributeSet")
        name_element = create_sub_element(self.element, "gen", "name")
        name_element.text = name
        for attribute in attributes:
            sub_element = create_sub_element(self.element, "gen", "genericAttribute")
            sub_element.append(attribute.element)


class DateAttribute(BaseFeature):
    def __init__(self, name, value):
        super().__init__("gen", "DateAttribute")
        name_element = create_sub_element(self.element, "gen", "name")
        name_element.text = name
        value_element = create_sub_element(self.element, "gen", "value")
        value_element.text = value.isoformat()


class DoubleAttribute(BaseFeature):
    def __init__(self, name, value):
        super().__init__("gen", "DoubleAttribute")
        name_element = create_sub_element(self.element, "gen", "name")
        name_element.text = name
        value_element = create_sub_element(self.element, "gen", "value")
        value_element.text = str(value)


class IntAttribute(BaseFeature):
    def __init__(self, name, value):
        super().__init__("gen", "IntAttribute")
        name_element = create_sub_element(self.element, "gen", "name")
        name_element.text = name
        value_element = create_sub_element(self.element, "gen", "value")
        value_element.text = str(value)


class StringAttribute(BaseFeature):
    def __init__(self, name, value):
        super().__init__("gen", "StringAttribute")
        name_element = create_sub_element(self.element, "gen", "name")
        name_element.text = name
        value_element = create_sub_element(self.element, "gen", "value")
        value_element.text = value
