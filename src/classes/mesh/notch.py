from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.gp import gp_Pnt, gp
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Extend.ShapeFactory import rotate_shape

class CylinderNotch:
    """
    A small shape at Z0 to be used to mark the cylinder
    """

    width = 1.0
    length = 3.5
    height = 0.5

    rotation = 270.0
    radius = 15.0

    def shape(self) -> TopoDS_Shape:
        # make the box shape
        start_x = self.radius - self.length
        point = gp_Pnt(start_x, 0.0, 0.0)
        box = BRepPrimAPI_MakeBox(point, self.length, self.width, self.height).Shape()

        # rotate the box along 0, 0, 1
        return rotate_shape(shape=box, axis=gp.OZ(), angle=self.rotation, unite="deg")