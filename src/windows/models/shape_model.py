from OCC.Core.TopoDS import TopoDS_Shape

class ShapeModel:

    def __init__(self, label: str, shape: TopoDS_Shape, rgb = (0.5, 0.5, 0.5)):

        self.label = label
        self.shape = shape
        self.rgb = rgb
