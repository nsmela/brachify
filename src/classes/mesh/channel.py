import numpy as np
import math

from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.gp import gp_Pnt, gp_Ax2
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone, BRepPrimAPI_MakeSphere
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_MakePipe
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.TopoDS import TopoDS_Shape

import classes.mesh.helper as helper

NEEDLE_LENGTH = 2.50


class NeedleChannel:
    def __init__(self, number: str, label: str, points):
        self.channel_number = number
        self.channel_label = label
        self.points = points
        self.points_raw = points
        self._shape = None

    def shape(self) -> TopoDS_Shape:
        if self._shape:
            return self._shape

        self._shape = rounded_channel(
            self.points, self._offset, self._diameter)
        #  self._shape = generate_curved_channel(self.points, self._offset, self._diameter)
        return self._shape

    def setChannel(self, height: float = 0.0, diameter: float = 3.0) -> None:
        self._offset = height
        self._diameter = diameter
        self._shape = None
        self.shape()

    def setDiameter(self, diameter: float) -> None:
        self._diameter = diameter
        self._shape = None
        self.shape()

    def setOffset(self, height: float = 0.0) -> None:
        self._offset = height
        self._shape = None
        self.shape()

    def getDiameter(self):
        return self._diameter

    def getOffset(self) -> float:
        return self._offset

    # ref:
    # https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    # https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors
    def getRotation(self):
        # calculate the sin angle on the xy plane using 0,0 and the highest point in the list of points
        v1 = [1.0, 0.0, self.points[0][2]]
        v2 = self.points[0]
        angle = math.atan2(v2[1] - v1[1], v2[0] - v1[0]) * \
            (180 / 3.14159)  # convert to degrees
        print(f"needle channel angle: {self.points[0]} : {angle}")

        # ensuring the angle stays between 0 and 360 degrees
        while angle < 0:
            angle += 360
            print(f"Small Angle! corrected to {angle}")

        while angle > 360:
            angle -= 360
            print(f"Large angle! corrected to {angle}")

        return angle

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
