from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Pnt, gp_Dir, gp_Circ, gp_Ax2
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone, BRepPrimAPI_MakeSphere
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.TopoDS import TopoDS_Shape

import src.Application.BRep.Helper as helper

import numpy as np

NEEDLE_LENGTH = 2.50


def rounded_channel(channel_points, offset: float = 0.0, diameter: float = 3.0) -> TopoDS_Shape:
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
        p_mid = gp_Pnt(p1.X() + vector.X(), p1.Y() +
                       vector.Y(), p1.Z() + vector.Z())
        cone = _cone_pipe(p1, p_mid, radius)
        pipe = _rounded_pipe(p_mid, p2, radius)
        pipe = BRepAlgoAPI_Fuse(cone, pipe).Shape()

    # rest of the points
    for i in range(1, len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        cylinder = _rounded_pipe(p1, p2, radius)
        pipe = BRepAlgoAPI_Fuse(pipe, cylinder).Shape()

    # curve downwards
    curve = _curved_end(points, radius)
    pipe = BRepAlgoAPI_Fuse(pipe, curve).Shape()

    # extend out of cylinder
    face = helper.get_lowest_face(pipe)
    extended_pipe = _extended_pipe(pipe)

    return extended_pipe


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


def _extended_pipe(shape: TopoDS_Shape) -> TopoDS_Shape:
    location = None

    lowest_face = helper.get_lowest_face(shape)
    if helper.face_is_plane(lowest_face):
        a_plane = helper.geom_plane_from_face(lowest_face)
        location = a_plane.Location()

    if location is None or location.Z() < 0:
        return shape

    extension = _straight_pipe(location, gp_Pnt(
        location.X(), location.Y(), -0.1), lowest_face)
    return BRepAlgoAPI_Fuse(shape, extension).Shape()


def _curved_end(points: list[gp_Pnt], radius: float) -> TopoDS_Shape:
    # add a curved pipe downwards using offset length and direction of last two points
    length = helper.get_magnitude(points[-2], points[-1])
    vector = helper.get_vector(points[-2], points[-1], length)
    p1 = points[-1]  # last point in array
    p2 = gp_Pnt(p1.X() + vector.X(), p1.Y() + vector.Y(),
                p1.Z() + vector.Z())  # middle point for bcurve
    # last point, lowered towards bottom
    p3 = gp_Pnt(p2.X(), p2.Y(), p2.Z() - length)

    # curve joining two straight paths
    array = TColgp_Array1OfPnt(1, 3)
    array.SetValue(1, p1)
    array.SetValue(2, p2)
    array.SetValue(3, p3)
    bz_curve = Geom_BezierCurve(array)
    bend_edge = BRepBuilderAPI_MakeEdge(bz_curve).Edge()

    # assembling the path
    wire = BRepBuilderAPI_MakeWire(bend_edge).Wire()

    # profile
    direction = helper.get_direction(p1, p2)
    profile = helper.circle_profile(p1, direction, radius)

    # shape using last face
    return BRepOffsetAPI_MakePipe(wire, profile).Shape()


def _rounded_pipe(p1: gp_Pnt, p2: gp_Pnt, radius: float) -> TopoDS_Shape:
    direction = helper.get_direction(p1, p2)
    profile = helper.circle_profile(p1, direction, radius)

    guide_edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    guide_wire = BRepBuilderAPI_MakeWire(guide_edge).Wire()

    cylinder = BRepOffsetAPI_MakePipe(guide_wire, profile).Shape()
    sphere = BRepPrimAPI_MakeSphere(p2, radius).Shape()
    return BRepAlgoAPI_Fuse(cylinder, sphere).Shape()
