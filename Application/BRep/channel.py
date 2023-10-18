from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Circ, gp_Ax2
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.TopoDS import TopoDS_Shape

import Application.BRep.Helper as helper

import numpy as np

NEEDLE_LENGTH = 2.50

def generate_curved_channel(points, offset: float = 0.0, diameter: float = 3.0) -> TopoDS_Shape:
    '''
    Generates a TopoDS_Shape from the Needle Channel's points
    Cylinder Offset is for height offset
    diameter is the channel's diameter
    '''

    if len(points) < 3:
        print(F"Needle Channel Generation error! needs 2 or more points!")
        return None

    # offset points using z axis and cylinder's offset
    # and convert into a gp_Pnt
    points = []
    for point in points:
        points.append(gp_Pnt(point[0], point[1], point[2] - offset))

    radius = diameter / 2

    # generate starting point on top (cone)
    p1 = points[0]
    p2 = points[1]
    length = helper.get_magnitude(p1, p2)
    if length < NEEDLE_LENGTH:
        pipe = _cone_pipe(p1, p2, radius)
    else:
        vector = helper.get_vector(p1, p2, length=NEEDLE_LENGTH)
        p_mid = gp_Pnt(p1.X() + vector.X(), p1.Y() + vector.Y(), p1.Z() + vector.Z())
        cone = _cone_pipe(p1, p_mid, radius)
        face = helper.get_lowest_face(cone)
        pipe = _straight_pipe(p_mid, p2, face)
        pipe = BRepAlgoAPI_Fuse(cone, pipe).Shape()
    face = helper.get_lowest_face(pipe)

    # for each (after the first), create a cylinder to next point to join
    for i in range(1, len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]

        cylinder = _straight_pipe(p1, p2, face)
        pipe = BRepAlgoAPI_Fuse(pipe, cylinder).Shape()
        face = helper.get_lowest_face(cylinder)

    # add a curved pipe downwards using offset length and direction of last two points
    length = helper.get_magnitude(points[-2], points[-1])
    vector = helper.get_vector(points[-2], points[-1], length)
    p1 = points[-1]  # last point in array
    p2 = gp_Pnt(p1.X() + vector.X(), p1.Y() + vector.Y(), p1.Z() + vector.Z())  # middle point for bcurve
    p3 = gp_Pnt(p2.X(), p2.Y(), p2.Z() - length)  # last point, lowered towards bottom

    # curve elbow after the points
    pipe_bend = _curved_pipe(p1, p2, p3, face)
    pipe = BRepAlgoAPI_Fuse(pipe, pipe_bend).Shape()

    # add a cylinder from pipe to past bottom of cylinder 
    base_point = gp_Pnt(p3.X(), p3.Y(), -10.0)
    face = helper.get_lowest_face(pipe)
    edge = BRepBuilderAPI_MakeEdge(p3, base_point).Edge()
    make_wire = BRepBuilderAPI_MakeWire(edge)
    make_wire.Build()
    wire = make_wire.Wire()
    cylinder = BRepOffsetAPI_MakePipe(wire, face).Shape()
    pipe = BRepAlgoAPI_Fuse(pipe, cylinder).Shape()

    return pipe


def sharp_needle_channel(channel_points, offset: float = 0.0, diameter: float = 3.0) -> TopoDS_Shape:
    """
    If a needle channel has a long distance between the first and second point, this helps stub it
    """
    if len(channel_points) < 3:
        print(F"Needle Channel Generation error! needs 3 or more points!")
        return None

        # offset points using z axis and cylinder's offset
        # and convert into a gp_Pnt
    points = []
    for point in channel_points:
        points.append(gp_Pnt(point[0], point[1], point[2] - offset))

    radius = diameter / 2

    # generate starting point on top (cone)
    p1 = points[0]
    p2 = points[1]
    length = helper.get_magnitude(p1, p2)
    if length < NEEDLE_LENGTH:
        pipe = _cone_pipe(p1, p2, radius)
    else:
        vector = helper.get_vector(p1, p2, length=NEEDLE_LENGTH)
        p_mid = gp_Pnt(p1.X() + vector.X(), p1.Y() + vector.Y(), p1.Z() + vector.Z())
        cone = _cone_pipe(p1, p_mid, radius)
        face = helper.get_lowest_face(cone)
        pipe = _straight_pipe(p_mid, p2, face)
        pipe = BRepAlgoAPI_Fuse(cone, pipe).Shape()
    face = helper.get_lowest_face(pipe)

    # smooth the points into a single curve
    p1 = points[1]  # the second point
    p2 = points[-1]  # the last point
    length = helper.get_magnitude(p1, p2)
    vector = helper.get_vector(p1, p2, length / 2)
    # curve points
    p3 = p2
    p2 = gp_Pnt(p1.X() + vector.X(), p1.Y() + vector.Y(), p1.Z() + vector.Z())  # middle point for bcurve

    # curve elbow after the points
    pipe_bend = _curved_pipe(p1, p2, p3, face)
    pipe = BRepAlgoAPI_Fuse(pipe, pipe_bend).Shape()

    # add a cylinder from pipe to past bottom of cylinder
    base_point = gp_Pnt(p3.X(), p3.Y(), -10.0)
    face = helper.get_lowest_face(pipe)
    edge = BRepBuilderAPI_MakeEdge(p3, base_point).Edge()
    make_wire = BRepBuilderAPI_MakeWire(edge)
    make_wire.Build()
    wire = make_wire.Wire()
    cylinder = BRepOffsetAPI_MakePipe(wire, face).Shape()
    pipe = BRepAlgoAPI_Fuse(pipe, cylinder).Shape()

    return pipe


def _cone_pipe(p1, p2, radius: float) -> TopoDS_Shape:
    length = helper.get_magnitude(p1, p2)
    direction = helper.get_direction(p1, p2)
    axis = gp_Ax2(p1, direction)
    return BRepPrimAPI_MakeCone(axis, 0.0, radius, length).Shape()


def _straight_pipe(p1, p2, face) -> TopoDS_Shape:
    edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    make_wire = BRepBuilderAPI_MakeWire(edge)
    make_wire.Build()
    wire = make_wire.Wire()
    return BRepOffsetAPI_MakePipe(wire, face).Shape()


def _curved_pipe(p1, p2, p3, face: TopoDS_Shape) -> TopoDS_Shape:
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
    return BRepOffsetAPI_MakePipe(wire, face).Shape()
