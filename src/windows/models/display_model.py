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
    
    def set_shape_colour(self, colours: dict, update=True):
        """
        colours is {label: [0.5, 0.5, 0.5]}
        """
        # colours is {label:rgb}
        for label, rgb in colours.items():
            self.colours[label] = rgb
        if update: self.update()

    def set_shape_visibility(self, visibility: dict, update: bool = True):
        """
        visibility is {label: bool} where True means the shape is passed to the display
        """
        self.visibility.update(visibility)
        if update: self.update()

    def update(self):
        """
        To update the viewport's shapes
        """

        # remove hidden shapes
        shapes = self.shapes
        for label, visible in self.visibility:
            if not visible and label in shapes.keys():
                del shapes[label]       

        # colour remaining shapes
        for label, rgb in self.colours.items():
            if label in shapes.keys():
                shapes[label].rgb = rgb
        self.shapes_changed.emit(list(shapes.values()), True)

    def __init__(self):
        super().__init__()
        self.colours = {}  # label: rgb
        self.visibility = {}  # label: bool where True is visible
        self.shapes = {}  # each entry stored as (ShapeModel)


