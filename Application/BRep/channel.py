from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Circ, gp_Ax2
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.TopoDS import TopoDS_Shape

from Core.Models.NeedleChannel import NeedleChannel
import Application.BRep.Helper as helper

import numpy as np


def generate_curved_channel(channel: NeedleChannel, cylinder_offset: float, diameter: float = 3.0) -> TopoDS_Shape:
    '''
    Generates a TopoDS_Shape from the Needle Channel's points
    Cylinder Offset is for height offset
    diameter is the channel's diameter
    '''
    # offset points using z axis and cylinder's offset
    # and convert into a gp_Pnt
    points = []
    for point in channel.points:
        points.append(gp_Pnt(point[0], point[1], point[2] - cylinder_offset))
    
    radius = diameter /2 
    
    # generate starting point on top (cone)
    p1 = points[0]
    p2 = points[1]
    vector = np.array([channel.points[1][0], channel.points[1][1], channel.points[1][2]]) \
        - np.array([channel.points[0][0], channel.points[0][1], channel.points[0][2]])
    length = np.linalg.norm(vector)
    direction = helper.get_direction(p1, p2)
    axis = gp_Ax2(p1, direction)
    pipe = BRepPrimAPI_MakeCone(axis, 0.0, radius, length).Shape()
    face = helper.get_lowest_face(pipe)
    
    # for each (after the first), create a sphere and cylinder to next point to join
    for i in range(1, len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        
        edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
        makeWire = BRepBuilderAPI_MakeWire(edge)
        makeWire.Build()
        wire = makeWire.Wire()
        cylinder = BRepOffsetAPI_MakePipe(wire, face).Shape()
        pipe = BRepAlgoAPI_Fuse(pipe, cylinder).Shape()
        face = helper.get_lowest_face(cylinder)

    # add a curved pipe downwards using offset length and direction of last two points
    vector = helper.get_vector(points[-2], points[-1], length + channel.curve_downwards)
    p1 = points[-1]
    p2 = gp_Pnt(p1.X() + vector.X(), p1.Y() + vector.Y(), p1.Z() + vector.Z())
    p3 = gp_Pnt(p2.X(), p2.Y(), p2.Z() - length - channel.curve_downwards)
    
    # curve joining two straight paths
    array = TColgp_Array1OfPnt(1, 3)
    array.SetValue(1, p1)
    array.SetValue(2, p2)
    array.SetValue(3, p3)
    bz_curve = Geom_BezierCurve(array)
    bend_edge = BRepBuilderAPI_MakeEdge(bz_curve).Edge()
    
    # assembling the path
    wire = BRepBuilderAPI_MakeWire(bend_edge).Wire()
    
    # shape using last face
    pipe_bend = BRepOffsetAPI_MakePipe(wire, face).Shape()
    pipe = BRepAlgoAPI_Fuse(pipe, pipe_bend).Shape()
    
    # add a cylinder from pipe to past bottom of cylinder 
    base_point = gp_Pnt(p3.X(), p3.Y(), -0.01)
    face = helper.get_lowest_face(pipe_bend)
    edge = BRepBuilderAPI_MakeEdge(p3, base_point).Edge()
    makeWire = BRepBuilderAPI_MakeWire(edge)
    makeWire.Build()
    wire = makeWire.Wire()
    cylinder = BRepOffsetAPI_MakePipe(wire, face).Shape()
    pipe = BRepAlgoAPI_Fuse(pipe, cylinder).Shape()

    return pipe