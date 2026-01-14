import logging

from model.city_object import CityObject

logger = logging.getLogger(__name__)


class GenericOccupiedSpace(CityObject):
    def __init__(self, ifc_element):
        super().__init__("gen", "GenericOccupiedSpace", ifc_element)
