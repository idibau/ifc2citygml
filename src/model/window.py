from model.filling import Filling


class Window(Filling):
    def __init__(self, ifc_entity, predefined_type):
        super().__init__("con", "Window", ifc_entity, predefined_type)
