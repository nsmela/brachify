from PySide6.QtCore import QObject, Signal

from .shape_model import ShapeModel, ShapeTypes
from classes.app import get_app
from classes.logger import log

default_colours = {
    ShapeTypes.CYLINDER: [1.0, 1.0, 1.0],
    ShapeTypes.CHANNEL: [0.2, 0.55, 0.55],
    ShapeTypes.TANDEM: [1.0, 1.0, 1.0]}


class DisplayModel(QObject):

    shapes_changed = Signal(list, bool)

    def add_shape(self, shape: ShapeModel):
        self.shapes[shape.label] = shape
        self.update()

    def add_shapes(self, shapes:list):
        for shape in shapes:
            self.shapes[shape.label] = shape
        self.update()

    def set_selected_shapes(self, shapes):
        log.debug(f"selecting {shapes} \n\n{shapes[0].DumpJsonToString()}")
        label = ""

        # each shape is set to not selected 
        # then set to selected if found
        for label, old_shape in self.shapes.items():
            self.shapes[label].selected = False  # if not found, stay False
            if shapes[0].IsEqual(old_shape.shape):
                self.shapes[old_shape.label].selected = True
                continue

        log.debug(f"shape matches {label}")
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
        colours is {ShapeTypes: [0.5, 0.5, 0.5]}
        """
        self.colours = colours
        
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
        for shape in shapes.values():
            if shape.selected: 
                shape.rgb = self.colours[ShapeTypes.SELECTED]
            else: 
                shape.rgb = self.colours[shape.type]
        self.shapes_changed.emit(list(shapes.values()), True)

    def __init__(self):
        super().__init__()
        self.colours = default_colours
        self.visibility = {}  # label: bool where True is visible
        self.shapes = {}  # each entry stored as (ShapeModel)

        # signals and slots
        # connected under initViews() in MainWindow class
