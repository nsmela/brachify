import math
import numpy as np

from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakePrism
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods, TopoDS_Face, TopoDS_Shape
from OCC.Core.gp import gp_Dir, gp_Ax2, gp_Pnt, gp_Pln, gp_Vec, gp_Circ
from OCC.Extend.ShapeFactory import translate_shp, rotate_shape


def face_is_plane(face: TopoDS_Face) -> bool:
    """
    Returns True if the TopoDS_Face is a plane, False otherwise
    """
    surf = BRepAdaptor_Surface(face, True)
    surf_type = surf.GetType()
    return surf_type == GeomAbs_Plane


def geom_plane_from_face(face: TopoDS_Face) -> gp_Pln:
    """
    Returns the geometric plane entity from a planar surface
    """
    return BRepAdaptor_Surface(face, True).Plane()


def get_faces(shape: TopoDS_Shape) -> list[TopoDS_Face]:
    '''
    returns a list of planar faces for the shape from highest to lowest
    '''

    def sortByZ(elem):
        return elem[1]

    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    faces = []
    while explorer.More():
        face = topods.Face(explorer.Current())
        if face_is_plane(face):
            a_plane = geom_plane_from_face(face)
            # face with it's z height
            faces.append([face, a_plane.Location().Z()])
        explorer.Next()
    faces.sort(key=sortByZ)
    return faces


def get_faces_axis(shape: TopoDS_Shape) -> list:
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    faces = []
    while explorer.More():
        face = topods.Face(explorer.Current())
        if face_is_plane(face):
            a_plane = geom_plane_from_face(face)
            faces.append([face, a_plane.Axis(), a_plane.Location()])
        explorer.Next()
    return faces


def lowest_face_by_normal(shape: TopoDS_Shape) -> TopoDS_Face:
    faces = get_faces_axis(shape)

    # check for a negative normal direction
    for face in faces:
        if face[1].Direction().Z() < 0.0:
            return face

    # check for the lowest face
    def sortByZ(elem):
        return elem[2].Z()

    faces.sort(key=sortByZ)
    return faces[0]


def get_highest_face(shape: TopoDS_Shape) -> TopoDS_Face:
    faces = get_faces(shape)
    return faces[-1][0]


def get_lowest_face(shape: TopoDS_Shape) -> TopoDS_Face:
    faces = get_faces(shape)
    return faces[0][0]


def get_vector(p1: gp_Pnt, p2: gp_Pnt, length: float = 1.0) -> gp_Vec:
    vector = gp_Vec(
        p2.X() - p1.X(),
        p2.Y() - p1.Y(),
        p2.Z() - p1.Z())
    return vector.Normalized() * length


def get_magnitude(p1: gp_Pnt, p2: gp_Pnt) -> float:
    vector = np.array([p2.X(), p2.Y(), p2.Z()]) \
        - np.array([p1.X(), p1.Y(), p1.Z()])
    return np.linalg.norm(vector)


def get_direction(p1: gp_Pnt, p2: gp_Pnt) -> gp_Dir:
    vector = get_vector(p1, p2)
    return gp_Dir(vector.X(), vector.Y(), vector.Z())


def get_vector_from_angle(v1: gp_Vec = gp_Vec(1, 0, 0), angle: float = 0.0, length: float = 1.0) -> gp_Vec:
    x = math.cos(angle)
    y = math.sin(angle)
    result = gp_Vec(v1.X() + x, v1.Y(), v1.Z()).Normalized()
    return result * length


def extend_bottom_face(shape: TopoDS_Shape) -> TopoDS_Shape:
    face = lowest_face_by_normal(shape)
    z = face[2].Z()
    direction = gp_Vec(0, 0, -z - 0.1)
    extended_geometry = BRepPrimAPI_MakePrism(face[0], direction).Shape()
    return BRepAlgoAPI_Fuse(shape, extended_geometry).Shape()


def translate_shape(shape: TopoDS_Shape, vector: gp_Vec) -> TopoDS_Shape:
    return translate_shp(shape, vector).Shape()


def rotate_shape(shape: TopoDS_Shape, rotation: gp_Vec) -> TopoDS_Shape:
    pass


def rotate_points(points, v_1, v_2):
    # V1 is the current vector which the coordinate system is aligned to
    # V2 is the vector we want the system aligned to
    # Points is an (n,3) array of n points (x,y,z)
    v_1 = np.asarray(v_1)
    v_2 = np.asarray(v_2)

    # Normalize V1 and V2 in case they aren't already
    len_1 = (v_1[0] ** 2 + v_1[1] ** 2 + v_1[2] ** 2) ** 0.5
    len_2 = (v_2[0] ** 2 + v_2[1] ** 2 + v_2[2] ** 2) ** 0.5
    v_1 = v_1 / len_1
    v_2 = v_2 / len_2

    if np.array_equal(v_1, v_2):  # points do not need to be rotated
        return points

    # Calculate the vector cross product
    cross_v1v2 = np.cross(v_1, v_2)
    cross_norm = (cross_v1v2[0] ** 2 + cross_v1v2[1]
                  ** 2 + cross_v1v2[2] ** 2) ** 0.5
    cross_normalized = cross_v1v2 / cross_norm

    # Dot product
    dot_v1v2 = np.dot(v_1, v_2)
    v1_norm = (v_1[0] ** 2 + v_1[1] ** 2 + v_1[2] ** 2) ** 0.5
    v2_norm = (v_2[0] ** 2 + v_2[1] ** 2 + v_2[2] ** 2) ** 0.5

    # Angle between the vectors
    theta = np.arccos(dot_v1v2 / (v1_norm * v2_norm))

    # Using Rodrigues' rotation formula (wikipedia):
    e = cross_normalized

    pts_rotated = np.empty((len(points), 3))
    if np.size(points) == 3:
        p = points
        p_rotated = np.cos(theta) * p + np.sin(theta) * \
            (np.cross(e, p)) + (1 - np.cos(theta)) * np.dot(e, p) * e
        pts_rotated = p_rotated
    else:
        for i, p in enumerate(points):
            p_rotated = np.cos(theta) * p + np.sin(theta) * \
                (np.cross(e, p)) + (1 - np.cos(theta)) * np.dot(e, p) * e
            pts_rotated[i] = p_rotated
    return pts_rotated


def circle_profile(origin: gp_Pnt, direction: gp_Vec, radius: float) -> TopoDS_Face:
    circle = gp_Circ(gp_Ax2(origin, direction), radius)
    edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    wire = BRepBuilderAPI_MakeWire(edge).Wire()
    return BRepBuilderAPI_MakeFace(wire).Face()


def add_point_and_vector(p1: gp_Pnt, v1: gp_Vec) -> gp_Pnt:
    return gp_Pnt(
        p1.X() + v1.X(),
        p1.Y() + v1.Y(),
        p1.Z() + v1.Z())
