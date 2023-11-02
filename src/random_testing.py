from OCC.Core.gp import *
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace, BRepBuilderAPI_MakeSolid
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.GC import GC_MakeArcOfCircle
from OCC.Core.BRepFill import BRepFill_PipeShell

import sys
#sys.path.append("src\Application\BRep\Tandem.py")

from Application.BRep import Tandem
from OCC.Display.SimpleGui import init_display

import math

display, start_display, add_menu, add_function_to_menu = init_display()


def evolved_shape():
    # specs
    angle = 45
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
    # b = y - mx
    x = tip_radius - radius
    if x > p3.X():
        x = p3.X()
        print(f"x was too large and was changed to: {x}")
    y = get_y_on_line(x, slope, b)
    p5 = gp_Pnt(x, 0, y)
    
    b = get_line_offset(p4, slope)
    y = get_y_on_line(x, slope, b)
    p6 = gp_Pnt(x, 0, y)
    edge5 = BRepBuilderAPI_MakeEdge(p5, p6).Edge()

    # used to calculate the ellipse
    straight_wire = BRepBuilderAPI_MakeWire(edge1, edge2).Wire()
    curve_wire = BRepBuilderAPI_MakeWire(edge3).Wire()

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p0, gp_Dir(0,0,1)), radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    pipe_straight = BRepFill_PipeShell(straight_wire)
    pipe_straight.Add(circle_wire)
    pipe_straight.Build()
    pipe_straight.MakeSolid()
    pipe = pipe_straight.Shape()

    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p1, gp_Dir(0,0,1)), radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    pipe_curved = BRepFill_PipeShell(curve_wire)
    pipe_curved.Add(circle_wire)
    pipe_curved.Build()
    pipe_curved.MakeSolid()
    pipe = BRepAlgoAPI_Fuse(pipe, pipe_curved.Shape()).Shape()

    slope, b = get_perpindicular_line(p3, p4)
    y = get_y_on_line(0, slope, b)
    p7 = gp_Pnt(0, 0, y)
    edge6 = BRepBuilderAPI_MakeEdge(p3, p7).Edge()
    edge7 = BRepBuilderAPI_MakeEdge(p1, p7).Edge()
    wire = BRepBuilderAPI_MakeWire(edge3, edge6, edge7).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    prism = BRepPrimAPI_MakePrism(face, gp_Vec(0, radius, 0)).Shape()
    prism = BRepAlgoAPI_Fuse(prism, BRepPrimAPI_MakePrism(face, gp_Vec(0, -radius, 0)).Shape()).Shape()
    pipe = BRepAlgoAPI_Fuse(pipe, prism).Shape()

    # upper half
    ## end of curve
    circle_edge = BRepBuilderAPI_MakeEdge(gp_Circ(gp_Ax2(p3, gp_Dir(vec)), tip_radius))
    circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge()).Wire()
    wire = BRepBuilderAPI_MakeWire(edge4).Wire()
    pipe_tip = BRepFill_PipeShell(wire)
    pipe_tip.Add(circle_wire)
    pipe_tip.Build()
    pipe_tip.MakeSolid()
    pipe_tip = BRepBuilderAPI_MakeSolid(pipe_tip.Shape()).Shape()

    ## space between tips
    edge7 = BRepBuilderAPI_MakeEdge(p3, p5).Edge()
    edge8 = BRepBuilderAPI_MakeEdge(p4, p6).Edge()
    wire = BRepBuilderAPI_MakeWire(edge4, edge8, edge5, edge7).Wire()
    face = BRepBuilderAPI_MakeFace(wire).Face()
    prism = BRepPrimAPI_MakePrism(face, gp_Vec(0, tip_radius, 0)).Shape()
    pipe_tip = BRepAlgoAPI_Fuse(pipe_tip, prism).Shape()
    prism = BRepPrimAPI_MakePrism(face, gp_Vec(0, -tip_radius, 0)).Shape()
    pipe_tip = BRepAlgoAPI_Fuse(pipe_tip, prism).Shape()

    ## tip on straight cylinder
    ## elliptical
    slope, b = get_perpindicular_line(p3, p4)
    x = -radius  #  edge of the first cylinder
    y = get_y_on_line(x, slope, b) - p5.Z()
    x = p5.X() + radius
    major_radius = math.sqrt(x**2 + y**2) #  calculate hypotenuse
    minor_radius = tip_radius
    if major_radius < minor_radius: major_radius = minor_radius + 0.1

    ellipse_edge = BRepBuilderAPI_MakeEdge(gp_Elips(gp_Ax2(p5, gp_Dir(vec)), major_radius, minor_radius)).Edge()
    ellipse_wire = BRepBuilderAPI_MakeWire(ellipse_edge).Wire()
    ellipse_face = BRepBuilderAPI_MakeFace(ellipse_wire).Face()
    eliipse_pipe = BRepPrimAPI_MakePrism(ellipse_face, gp_Vec(0, 0, p6.Z() - p5.Z())).Shape()
    pipe_tip = BRepAlgoAPI_Fuse(pipe_tip, eliipse_pipe).Shape()

    pipe = BRepAlgoAPI_Fuse(pipe, pipe_tip).Shape()
    display.DisplayShape(pipe)
    

def tandem_shape():
    shape = Tandem.generate_tandem()
    display.DisplayShape(shape)


if __name__ == "__main__":
    #evolved_shape()
    tandem_shape()
    start_display()