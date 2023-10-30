from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire
from OCC.Core.gp import *

import Helper as helper

# generates a custom tandem with inputs

def generate_tandem(
        channel_diameter: float = 4.0,
        tip_diameter: float = 8.0,
        tip_thickness: float = 4.0,
        tip_angle = 60.0,
        tip_height: float = 150.0) -> TopoDS_Shape:
    
    # create cylinder from bottom to neck height
    cylinder = BRepPrimAPI_MakeCylinder(r=channel_diameter, h=tip_height).Shape()


    # create profile for tip using angle, tip thickness

    # extrude profile using tip radius
    # fillet the extrusion
    # fuse the two


    # or....
    
    p1 = gp_Pnt(channel_diameter, channel_diameter, 0.10)
    p2 = gp_Pnt(channel_diameter, channel_diameter, tip_height)
    edge = BRepBuilderAPI_MakeEdge(p1, p2).Edge()
    wire = BRepBuilderAPI_MakeWire()
    wire.Add(edge)
    
    angle_vector = helper.get_vector_from_angle(angle=tip_angle)
    p3 = p2 + (angle_vector * (tip_thickness))
    p4 = p2 + (angle_vector * (tip_thickness * 2))


    pass