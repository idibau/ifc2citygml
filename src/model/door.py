from model.filling import Filling


class Door(Filling):
    def __init__(self, ifc_element):
        super().__init__("con", "Door", ifc_element)
