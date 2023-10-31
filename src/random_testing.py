from OCC.Core.gp import gp_Pnt, gp_Circ, gp_Dir, gp_Ax2, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.GeomAbs import GeomAbs_Arc
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeEvolved
from OCC.Core.GC import GC_MakeArcOfCircle
from OCC.Core.BRepFill import BRepFill_PipeShell

from OCC.Display.SimpleGui import init_display

import math

display, start_display, add_menu, add_function_to_menu = init_display()


def evolved_shape():
    angle = math.radians(90) 
    height = 160
    length = 200
    length_offset = 20.0
    radius_offset = 35.0
    radius = 15.0

    p0 = gp_Pnt(0,0,0)
    p1 = gp_Pnt(0,0,height)
    edge1 = BRepBuilderAPI_MakeEdge(p0, p1).Edge()

    p2 = gp_Pnt(0,0,length + length_offset)
    edge2 = BRepBuilderAPI_MakeEdge(p1,p2).Edge()

    direction = gp_Vec(0, 0, 1)
    x = radius - math.cos(angle) * radius_offset
    y = math.sin(angle) * 0
    p3 = gp_Pnt(x, 0, length + y)

    arc = GC_MakeArcOfCircle(p1, direction, p3)
    edge3 = BRepBuilderAPI_MakeEdge(arc.Value()).Edge()

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p0, gp_Dir(0,0,1)), radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    profile = BRepBuilderAPI_MakeFace(circle_wire).Face()
    
    straight_wire = BRepBuilderAPI_MakeWire(edge1, edge2).Wire()
    curve_wire = BRepBuilderAPI_MakeWire(edge3).Wire()

    pipe_straight = BRepFill_PipeShell(straight_wire)
    pipe_straight.Add(circle_wire)
    pipe_straight.Build()
    display.DisplayShape(pipe_straight.Shape(), update=False)

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p1, gp_Dir(0,0,1)), radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    pipe_curved = BRepFill_PipeShell(curve_wire)
    pipe_curved.Add(circle_wire)
    pipe_curved.Build()
    display.DisplayShape(pipe_curved.Shape(), update=True)

if __name__ == "__main__":
    evolved_shape()
    start_display()