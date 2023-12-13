from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
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
    SELECTED = auto()
    EXPORT = auto()
    

class ShapeModel:

    def isMatch(self, compounds: list) -> bool:
        for compound in compounds:
            # skip objects that are not 
            if type(compound) is not \
            type(TopoDS_Compound) and type(TopoDS_Shape): 
                continue

            if compound.IsEqual(self.shape): return True
        
        return False

    def __init__(self, label: str, shape: TopoDS_Shape, shape_type: ShapeTypes):

        self.label = label
        self.shape = shape
        self.type = shape_type or ShapeTypes.NONE  # flags the shape
        self.rgb = None  # used by display model and viewport

        # flags
        self.selected = False
        self.transparent = False
        self.enabled = True
    

