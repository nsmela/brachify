from tkinter import EXTENDED
from OCC.Core.BRepAdaptor import BRepAdaptor_Surface
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut, BRepAlgoAPI_Fuse
from OCC.Core.BRepFilletAPI import BRepFilletAPI_MakeFillet
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeTorus, BRepPrimAPI_MakePrism
from OCC.Core.GeomAbs import GeomAbs_Plane
from OCC.Core.TopAbs import TopAbs_FACE
from OCC.Core.TopExp import TopExp_Explorer
from OCC.Core.TopoDS import topods, TopoDS_Face, TopoDS_Solid, TopoDS_Shape
from OCC.Core.gp import gp_Dir, gp_Ax2, gp_Pnt, gp_Pln, gp_Vec
from OCC.Extend.TopologyUtils import TopologyExplorer
from OCC.Extend.ShapeFactory import translate_shp


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
            faces.append([face, a_plane.Location().Z()]) # face with it's z height
        explorer.Next()
    faces.sort(key=sortByZ)
    return faces


def get_faces_axis(shape:TopoDS_Shape)-> list:
    explorer = TopExp_Explorer(shape, TopAbs_FACE)
    faces = []
    while explorer.More():
         face = topods.Face(explorer.Current())
         if face_is_plane(face):
                a_plane = geom_plane_from_face(face)
                faces.append([face, a_plane.Axis(), a_plane.Location()])
         explorer.Next()
    return faces


def lowest_face_by_normal(shape:TopoDS_Shape) -> TopoDS_Face:
    for face in get_faces_axis(shape):
        if face[1].Direction().Z() < 0.0:
            return face
    return None

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


def get_direction(p1: gp_Pnt, p2: gp_Pnt) -> gp_Dir:
    vector = get_vector(p1, p2)
    return gp_Dir(vector.X(), vector.Y(), vector.Z())


def extend_bottom_face(shape:TopoDS_Shape) -> TopoDS_Shape:
    face = lowest_face_by_normal(shape) #get_lowest_face(shape)
    z = face[2].Z() #geom_plane_from_face(face).Location().Z()
    direction = gp_Vec(0,0, -z - 0.1)
    extended_geometry = BRepPrimAPI_MakePrism(face[0], direction).Shape()
    return BRepAlgoAPI_Fuse(shape, extended_geometry).Shape()