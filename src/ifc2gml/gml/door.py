from ifc2gml.gml.filling import Filling


class Door(Filling):
    def __init__(self):
        super().__init__("con", "Door")
