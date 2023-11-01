from OCC.Core.gp import gp_Pnt, gp_Circ, gp_Dir, gp_Ax2, gp_Vec
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakePolygon, BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeSolid
from OCC.Core.GeomAbs import GeomAbs_Arc
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakeEvolved, BRepOffsetAPI_ThruSections
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
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
    radius_offset = 35.0
    radius = 5.0
    tip_thickness = 20.0
    tip_radius = 8


    def get_perpindicular_slope(p1, p2):
        m = (p2.Z() - p1.Z()) / (p2.X() - p1.X())     
        return -1 / m

    def get_line_offset(p1, slope):
        return p1.Z() - (slope * p1.X())

    def get_perpindicular_line(p1, p2):
        slope = get_perpindicular_slope(p1, p2)
        b = get_line_offset(p1, slope)
        return slope, b
    
    def get_y_on_line(x, slope, b):
        return slope * x + b

    # initial tube from origin to designated height
    p0 = gp_Pnt(0,0,0)
    p1 = gp_Pnt(0,0,height)
    edge1 = BRepBuilderAPI_MakeEdge(p0, p1).Edge()

    # extra length on the straight tube going outside the cylinder
    p2 = gp_Pnt(0,0,length)
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
    slope, b = get_perpindicular_line(p3, p4)
    print(f"p3 = {p3.X()}, {p3.Z()}")
    print(f"p4 = {p4.X()}, {p4.Z()}")
    print(f"slope(m): {slope}")
    print(f"b = {b}")

    # b = y - mx
    x = tip_radius - radius
    print(f"x = {x}")
    if x > p3.X():
        x = p3.X()
        print(f"x was too large and was changed to: {x}")
    y = get_y_on_line(x, slope, b)
    print(f"y = {y}")
    p5 = gp_Pnt(x, 0, y)
    
    b = get_line_offset(p4, slope)
    y = get_y_on_line(x, slope, b)
    p6 = gp_Pnt(x, 0, y)
    edge5 = BRepBuilderAPI_MakeEdge(p5, p6).Edge()



    
    straight_wire = BRepBuilderAPI_MakeWire(edge1, edge2).Wire()
    curve_wire = BRepBuilderAPI_MakeWire(edge3).Wire()

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p0, gp_Dir(0,0,1)), radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    pipe_straight = BRepFill_PipeShell(straight_wire)
    pipe_straight.Add(circle_wire)
    pipe_straight.Build()
    pipe_straight.MakeSolid()
    #display.DisplayShape(pipe_straight.Shape())
    display.DisplayShape(straight_wire)

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p1, gp_Dir(0,0,1)), radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    pipe_curved = BRepFill_PipeShell(curve_wire)
    pipe_curved.Add(circle_wire)
    pipe_curved.Build()
    pipe_curved.MakeSolid()
    #display.DisplayShape(pipe_curved.Shape())
    display.DisplayShape(curve_wire)

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p3, gp_Dir(vec)), tip_radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    wire = BRepBuilderAPI_MakeWire(edge4).Wire()
    pipe_tip = BRepFill_PipeShell(wire)
    pipe_tip.Add(circle_wire)
    pipe_tip.Build()
    pipe_tip.MakeSolid()
    pipe_tip_shape = BRepBuilderAPI_MakeSolid(pipe_tip.Shape()).Shape()
    #display.DisplayShape(pipe_tip_shape)
    display.DisplayShape(wire)

    wire = BRepBuilderAPI_MakeWire(edge5).Wire()
    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p5, gp_Dir(vec)), tip_radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    circle_edge2 = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p6, gp_Dir(vec)), tip_radius))
    circle_wire2 = BRepBuilderAPI_MakeWire(circle_edge2.Edge()).Wire()   
    pipe_tip2 = BRepOffsetAPI_ThruSections()
    pipe_tip2.AddWire(circle_wire)
    pipe_tip2.AddWire(circle_wire2)
    #display.DisplayShape(pipe_tip2.Shape())
    display.DisplayShape(wire)

    # making polygons to fill spaces between cylinders
    # lower half
    # edge from edge1 to bottom of tandem tips
    slope, b = get_perpindicular_line(p3, p4)
    y = get_y_on_line(0, slope, b)
    p7 = gp_Pnt(0, 0, y)
    edge6 = BRepBuilderAPI_MakeEdge(p3, p7).Edge()
    edge7 = BRepBuilderAPI_MakeEdge(p1, p7).Edge()
    wire = BRepBuilderAPI_MakeWire(edge3, edge6, edge7).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    prism = BRepPrimAPI_MakePrism(face, gp_Vec(0, radius, 0)).Shape()
    prism = BRepAlgoAPI_Fuse(prism, BRepPrimAPI_MakePrism(face, gp_Vec(0, -radius, 0)).Shape()).Shape()
    display.DisplayShape(prism)

    # upper half
    edge7 = BRepBuilderAPI_MakeEdge(p3, p5).Edge()
    edge8 = BRepBuilderAPI_MakeEdge(p4, p6).Edge()
    wire = BRepBuilderAPI_MakeWire(edge4, edge8, edge5, edge7).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    prism = BRepPrimAPI_MakePrism(face, gp_Vec(0, tip_radius, 0)).Shape()
    prism = BRepAlgoAPI_Fuse(prism, BRepPrimAPI_MakePrism(face, gp_Vec(0, -tip_radius, 0)).Shape()).Shape()
    display.DisplayShape(prism)
    

if __name__ == "__main__":
    evolved_shape()
    start_display()