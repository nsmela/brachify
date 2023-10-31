from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import *

import Application.BRep.Helper as helper
import numpy as np


# generates a custom tandem with inputed values
def generate_tandem(
        channel_diameter: float = 4.0,
        tip_diameter: float = 8.0,
        tip_thickness: float = 4.0,
        tip_angle = 60.0,
        tip_height: float = 150.0) -> TopoDS_Shape:
    
    # create cylinder from bottom to neck height
    cylinder = BRepPrimAPI_MakeCylinder(channel_diameter, tip_height).Shape()


    # create profile for tip using angle, tip thickness

    # extrude profile using tip radius
    # fillet the extrusion
    # fuse the two
    return cylinder


def generate_tandem_from_faces(
        channel_diameter: float = 4.0,
        tip_diameter: float = 8.0,
        tip_thickness: float = 4.0,
        tip_angle = 60.0,
        tip_height: float = 150.0) -> TopoDS_Shape:
    # or... build a shape, extrude it and fillet it
    p1 = gp_Pnt(channel_diameter, -channel_diameter, 0.10)
    p2 = gp_Pnt(channel_diameter, -channel_diameter, tip_height)
    edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    wire = BRepBuilderAPI_MakeWire()
    wire.Add(edge)

    # curve for the angle    
    angle_vector = helper.get_vector_from_angle(angle=tip_angle)
    p3 = helper.add_point_and_vector(p2, (angle_vector * (tip_thickness)))
    p4 = helper.add_point_and_vector(p2, (angle_vector * (tip_thickness * 2)))

    array = TColgp_Array1OfPnt(1, 3)
    array.SetValue(1, p2)
    array.SetValue(2, p3)
    array.SetValue(3, p4)
    bz_curve = Geom_BezierCurve(array)
    bend_edge = BRepBuilderAPI_MakeEdge(bz_curve).Edge()
    wire.Add(bend_edge)

    # flat top
    p5 = helper.add_point_and_vector(p4, (angle_vector * (tip_thickness)))
    edge = BRepBuilderAPI_MakeEdge(p4, p5).Edge()
    wire.Add(edge)

    angle_vector = helper.get_vector_from_angle(angle=tip_angle+90.0)
    p0 = gp_Pnt(-channel_diameter, -channel_diameter, 0.10)
    p6 = helper.add_point_and_vector(p5, (angle_vector * (tip_thickness)))  # need to calculate intersecting point
    backpoint = gp_Pnt(-channel_diameter, -channel_diameter, tip_height)  # used to calculate the intersection point
    p7 = intersecting_lines(p5, p6, p0, backpoint) 
    edge = BRepBuilderAPI_MakeEdge(p5, p7).Edge()
    wire.Add(edge)

    edge = BRepBuilderAPI_MakeEdge(p7, p0).Edge()
    wire.Add(edge)

    edge = BRepBuilderAPI_MakeEdge(p0, p1).Edge()
    wire.Add(edge)

    return wire.Wire()


def intersecting_lines(p1a: gp_Pnt, p2a: gp_Pnt, p1b: gp_Pnt, p2b:gp_Pnt) -> gp_Pnt:
    """intersection of two lines on the XZ plane"""
    a1 = [p1a.X(), p1a.Z()]
    a2 = [p2a.X(), p2a.Z()]
    b1 = [p1b.X(), p1b.Z()]
    b2 = [p2b.X(), p2b.Z()]
    
    s = np.vstack([a1,a2,b1,b2])
    h = np.hstack((s, np.ones((4,1))))
    
    line1 = np.cross(h[0], h[1])
    line2 = np.cross(h[2], h[3])
    
    x, y, z = np.cross(line1, line2)

    if z == 0:  # if lines are parallel
        return None
    
    return gp_Pnt(x/z, p1a.Y(), y/z)