from model.filling import Filling


class Door(Filling):
    def __init__(self,  ifc_entity, predefined_type):
        super().__init__("con", "Door", ifc_entity, predefined_type)
