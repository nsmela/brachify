from OCC.Core.gp import gp_Pnt, gp_Circ, gp_Dir, gp_Ax2, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeSolid
from OCC.Core.GeomAbs import GeomAbs_Arc
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeEvolved
from OCC.Core.GC import GC_MakeArcOfCircle
from OCC.Core.BRepFill import BRepFill_PipeShell

from OCC.Display.SimpleGui import init_display

import math

display, start_display, add_menu, add_function_to_menu = init_display()


def evolved_shape():
    # specs
    angle = 30
    angle_rads = math.radians(angle) 
    height = 160
    length = 200
    length_offset = 20.0
    radius_offset = 35.0
    radius = 5.0
    tip_thickness = 20.0
    tip_radius = 8

    # initial tube from origin to designated height
    p0 = gp_Pnt(0,0,0)
    p1 = gp_Pnt(0,0,height)
    edge1 = BRepBuilderAPI_MakeEdge(p0, p1).Edge()

    # extra length on the straight tube going outside the cylinder
    p2 = gp_Pnt(0,0,length + length_offset)
    edge2 = BRepBuilderAPI_MakeEdge(p1,p2).Edge()

    # curved section to match tandem's tilt
    direction = gp_Vec(0, 0, 1)
    x = radius_offset - (math.cos(angle_rads) * radius_offset)
    y = math.sin(angle_rads) * radius_offset
    p3 = gp_Pnt(x, 0, height + y)

    arc = GC_MakeArcOfCircle(p1, direction, p3)
    edge3 = BRepBuilderAPI_MakeEdge(arc.Value()).Edge()

    # tandem's tip
    angle2 = 90 - angle
    
    x = math.cos(math.radians(angle2))
    y = math.sin(math.radians(angle2))
    vec = gp_Vec(x, 0, y) * tip_thickness
    p4 = gp_Pnt(p3.X() + vec.X(), p3.Y() + vec.Y(), p3.Z() + vec.Z())
    edge4 = BRepBuilderAPI_MakeEdge(p3, p4).Edge()

    # extending the tandem's tip
    # line formula is y = mx + b
    # slope formula is m = y2 - y1 / x2 - x1
    # slope perpindicular is -1 / m
    print(f"p3 = {p3.X()}, {p3.Z()}")
    print(f"p4 = {p4.X()}, {p4.Z()}")
    m = (p4.Z() - p3.Z()) / (p4.X() - p3.X()) 
    print(f"m = {m}")
    slope = -1 / m
    print(f"slope(m): {slope}")

    # b = y - mx
    b = p3.Z() - (slope * p3.X())
    print(f"b = {b}")
    x = tip_radius - radius
    print(f"x = {x}")
    if x > p3.X():
        x = p3.X()
        print(f"x was too large and was changed to: {x}")
    y = slope * x + b
    print(f"y = {y}")

    



    
    straight_wire = BRepBuilderAPI_MakeWire(edge1, edge2).Wire()
    curve_wire = BRepBuilderAPI_MakeWire(edge3).Wire()

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p0, gp_Dir(0,0,1)), radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    pipe_straight = BRepFill_PipeShell(straight_wire)
    pipe_straight.Add(circle_wire)
    pipe_straight.Build()
    pipe_straight.MakeSolid()
    display.DisplayShape(pipe_straight.Shape())

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p1, gp_Dir(0,0,1)), radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    pipe_curved = BRepFill_PipeShell(curve_wire)
    pipe_curved.Add(circle_wire)
    pipe_curved.Build()
    pipe_curved.MakeSolid()
    pipe = BRepBuilderAPI_MakeSolid(pipe_curved.Shape()).Shape()
    display.DisplayShape(pipe)

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p3, gp_Dir(vec)), tip_radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    pipe_tip = BRepFill_PipeShell(BRepBuilderAPI_MakeWire(edge4).Wire())
    pipe_tip.Add(circle_wire)
    pipe_tip.Build()
    pipe_tip.MakeSolid()
    pipe_tip_shape = BRepBuilderAPI_MakeSolid(pipe_tip.Shape()).Shape()
    display.DisplayShape(pipe_tip_shape)


if __name__ == "__main__":
    evolved_shape()
    start_display()