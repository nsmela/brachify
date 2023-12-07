from OCC.Core.TopoDS import TopoDS_Shape
from enum import Enum, auto, unique


@unique
class ShapeTypes(Enum):
    """
    used to flag details about the shape
    """
    NONE = auto()
    CYLINDER = auto()
    CHANNEL = auto()
    TANDEM = auto()
    

class ShapeModel:

    def __init__(self, label: str, shape: TopoDS_Shape, shape_type: ShapeTypes):

        self.label = label
        self.shape = shape
        self.type = shape_type or ShapeTypes.NONE  # flags the shape
        self.rgb = None  # used by display model and viewport

        # flags
        self.selected = False
        self.transparent = False

