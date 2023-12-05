from PySide6.QtCore import QObject, Signal
from .shape_model import ShapeModel


class DisplayModel(QObject):

    shapes_changed = Signal(list, bool)

    def add_shape(self, shape: ShapeModel):
        self.shapes[shape.label] = shape
        self.update()

    def add_shapes(self, shapes:list):
        for shape in shapes:
            self.shapes[shape.label] = shape
        self.update()

    def remove_shape(self, label:str):
        if label in self.shapes:
            self.shapes.pop(label)
        self.update()

    def remove_shapes(self, labels:list):
        for label in labels:
            self.shapes.pop(label)
        self.update()
    
    def set_shape_colour(self, colours: dict):
        # colours is {label:rgb}
        for label, rgb in colours.items():
            self.colours[label] = rgb
        self.update()

    def update(self):
        for label, rgb in self.colours.items():
            if label in self.shapes.keys():
                self.shapes[label].rgb = rgb
        self.shapes_changed.emit(list(self.shapes.values()), True)

    def __init__(self):
        super().__init__()
        self.colours = {}  # label: rgb
        self.shapes = {}  # each entry stored as (ShapeModel)


