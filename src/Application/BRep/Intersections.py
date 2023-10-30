# https://dev.opencascade.org/content/quickest-way-check-if-two-shapes-intersect
# https://old.opencascade.com/doc/occt-7.5.0/overview/html/occt_user_guides__modeling_algos.html
# https://github.com/tpaviot/pythonocc-core/issues/1259
# used to determine if  shape is intersecting any other shapes

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Section
from OCC.Core.TopoDS import TopoDS_Shape


def are_colliding(shape1: TopoDS_Shape, shape2: TopoDS_Shape) -> bool:
    collision_shapes = BRepAlgoAPI_Section(shape1, shape2)
    return collision_shapes.Shape().NbChildren() > 0


# TODO check for distances
# TODO create meshes and check for intersections that way
