from model.filling import Filling


class Window(Filling):
    def __init__(self, ifc_element):
        super().__init__("con", "Window", ifc_element)
