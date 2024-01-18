import math

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse, BRepAlgoAPI_Common
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepFill import BRepFill_PipeShell
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeSphere, BRepPrimAPI_MakePrism
from OCC.Core.GC import GC_MakeArcOfCircle, GC_MakeSegment
from OCC.Core.Geom2d import Geom2d_Circle, Geom2d_Line
from OCC.Core.Geom2dAPI import Geom2dAPI_InterCurveCurve
from OCC.Core.gp import *
from OCC.Core.TopoDS import TopoDS_Shape

# TODO create a step file that shows the points and measurements here to visualize what is being done
class Tandem():
    cylinder_height: float = 160.0
    cylinder_diameter: float = 15
    tandem_height: float = 129.0 # default
    tandem_diameter: float = 8.0
    tandem_angle: float = 60.0
    bend_radius: float = 35.0
    tandem_length: float = 8.0
    height_offset = 10.0

    stopper_enabled = True
    stopper_length = 8.0
    stopper_diameter = 12.0

    bend_end = gp_Pnt(0,0,0)
    bend_direction = gp_Dir(0,0,1)
    
    def cylinder_offset_shape(self) -> TopoDS_Shape:
        radius = self.cylinder_diameter / 2 + self.height_offset
        height = self.cylinder_height + self.height_offset - radius - 1

        top_point = gp_Pnt(0,0,self.cylinder_height)
        start_arc_point = gp_Pnt(-radius, 0, height)
        end_arc_point = gp_Pnt(radius, 0, height)
        bottom_point = gp_Pnt(radius, 0, 0)

        circle = gp_Circ(gp_Ax2(gp_Pnt(0,0, height), gp_Dir(0,1,0)), radius)
        curve = GC_MakeArcOfCircle(circle, start_arc_point, end_arc_point, True)
        line = GC_MakeSegment(end_arc_point, bottom_point)

        edges = []
        edges.append(BRepBuilderAPI_MakeEdge(curve.Value()).Edge())
        edges.append(BRepBuilderAPI_MakeEdge(line.Value()).Edge())
        edges.append(make_edge(bottom_point, gp_Pnt(-radius, 0, 0)))
        edges.append(make_edge(gp_Pnt(-radius, 0, 0), start_arc_point))
        wire = make_wire(edges)

        return make_symmetrical_shape(wire, radius)

    def generate_shape(self) -> TopoDS_Shape:
        # create tandem
        tandem = self.tandem_shape()
        # create stopper, if needed
        stopper = self.stopper_shape()
        # combine stopper to tandem
        shape = fuse_shapes([tandem, stopper])
        # create cylinder
        cylinder = self.cylinder_offset_shape()
        # union cylinder and tandem+stopper model
        return BRepAlgoAPI_Common(shape, cylinder).Shape()

    def stopper_shape(self) -> TopoDS_Shape:
        # create a slanted circle and extrude it upwards
        max_height = self.cylinder_height + self.height_offset
        stopper_depth = self.stopper_length
        stopper_radius = self.stopper_diameter / 2
        stopper_rads = math.radians(90 - self.tandem_angle)
        stopper_direction = gp_Dir(
            math.cos(stopper_rads),
            0,
            math.sin(stopper_rads))
        stopper_start = self.bend_end
        axis = gp_Ax2(stopper_start, stopper_direction)
        circle = gp_Circ(axis, stopper_radius)
        distance = max_height - stopper_start.Z()
        stopper_profile = BRepBuilderAPI_MakeFace(BRepBuilderAPI_MakeWire(BRepBuilderAPI_MakeEdge(circle).Edge()).Wire()).Face()
        channel_shape = BRepPrimAPI_MakePrism(stopper_profile, gp_Vec(0, 0, distance)).Shape()
        vector = gp_Vec(stopper_direction) * distance
        tandem_shape = BRepPrimAPI_MakePrism(stopper_profile, vector).Shape()

        stopper_line = Geom2d_Line(gp_Lin2d(gp_Pnt2d(stopper_start.X(), stopper_start.Z()), gp_Dir2d(stopper_direction.X(), stopper_direction.Z())))
        cylinder_radius = self.cylinder_diameter / 2 + self.height_offset
        arc_circle_origin = gp_Pnt2d(0, max_height - cylinder_radius)
        arc_circle = Geom2d_Circle(gp_Circ2d(gp_Ax2d(arc_circle_origin, gp_Dir2d(0,1)), cylinder_radius))
        arc_end = intersection2d(stopper_line, arc_circle)

        p0 = stopper_start
        p1 = gp_Pnt(stopper_start.X(), 0, max_height)
        p2 = to3d(arc_end)

        edges = []
        edges.append(make_edge(p0, p1))
        edges.append(make_edge(p1, p2))
        edges.append(make_edge(p2, p0))
        wire = make_wire(edges)
        shape = make_symmetrical_shape(wire, stopper_radius)

        return fuse_shapes([channel_shape, tandem_shape, shape])

    def tandem_shape(self) -> TopoDS_Shape:
        """
        Generate the points, edges, wires and then shapes for the tandem and outputs a shape
        """
        # variables used
        height_offset = self.height_offset  # tandem extends past cylinder by this amount
        max_height = self.cylinder_height + height_offset
        cylinder_radius = (self.cylinder_diameter)/2  + height_offset
        tandem_radius = self.tandem_diameter / 2

        tandem_height = self.tandem_height
        bend_radius = self.bend_radius

        #########################################################################################
        # 2D points    
        #########################################################################################
        origin = gp_Pnt2d(0,0)
        top_circle_origin = gp_Pnt(0, 0, max_height - cylinder_radius)  # circle origin for the top arc
        bend_start = gp_Pnt2d(0, tandem_height)
        bend_origin = gp_Pnt2d(bend_radius, tandem_height)  # point on the circle centre

        # bend end 
        # a line is angled with the tandem angle and the highest intersection is the bend's end
        bend_rads = math.radians(180-self.tandem_angle)
        x = math.cos(bend_rads)
        y = math.sin(bend_rads)
        bend_direction = gp_Dir2d(x, y)
        bend_circle = gp_Circ2d(gp_Ax22d(bend_origin, bend_direction), bend_radius)
        bend_line = gp_Lin2d(bend_origin, bend_direction)

        line_curve = Geom2d_Line(bend_line)
        bend_curve = Geom2d_Circle(bend_circle)
        intersection = Geom2dAPI_InterCurveCurve(bend_curve, line_curve)

        # highest intersecting point is the end of the bending section
        bend_end = gp_Pnt2d(0, -100)
        if intersection.NbPoints() < 1:
            raise Exception("Invalid bend!")
        else:
            for i in range(1, intersection.NbPoints() + 1):
                point = intersection.Point(i)
                if point.Y() > bend_end.Y():
                    bend_end = point

        # top tandem end
        # where the top arc intersects with the tandem leaving the cylinder
        # two possible situations:
        #   1) bend exits the cylinder: calculate the intersection of the two arcs
        #   2) bend ends within the cylinder: create a line that continues tangently and caluclate the intersection
        top_circle_origin = gp_Pnt2d(0, max_height - cylinder_radius)
        top_circle = gp_Circ2d(gp_Ax2d(top_circle_origin, gp_Dir2d(0, 1)), cylinder_radius)
        top_curve = Geom2d_Circle(top_circle)

        # if bend_end is outside the cylinder
        is_intersecting_bend = False
        if bend_end.Distance(top_circle_origin) < cylinder_radius \
                    or (bend_end.X() < cylinder_radius and bend_end.Y() < top_circle_origin.Y()):
            new_line = bend_line.Rotated(bend_end, math.radians(90))
            direction = new_line.Direction()
            tandem_final_line = Geom2d_Line(bend_end, direction)
            intersection = Geom2dAPI_InterCurveCurve(top_curve, tandem_final_line)
        else:
            is_intersecting_bend = True
            circle = Geom2d_Circle(bend_circle)
            intersection = Geom2dAPI_InterCurveCurve(top_curve, circle)       

        top_tandem_point = gp_Pnt2d(0, -100)
        if intersection.NbPoints() < 1:
            raise Exception("Tandem doesn't exit cylinder!")
        else:
            top_tandem_point = gp_Pnt2d(0, -100)
            for i in range(1, intersection.NbPoints() + 1):
                point = intersection.Point(i)
                if top_tandem_point.Y() < point.Y():
                    top_tandem_point = point

        #########################################################################################
        # 3D points    
        #########################################################################################
        def to_3d(point: gp_Pnt2d):
            return gp_Pnt(point.X(), 0, point.Y())

        bend_origin_3d = to_3d(bend_origin)
        bend_start_3d = to_3d(bend_start)
        bend_end_3d = to_3d(bend_end)
        top_3d = gp_Pnt(0, 0, max_height)
        top_arc_origin_3d = to_3d(top_circle_origin)
        tandem_end_3d = to_3d(top_tandem_point)

        #########################################################################################
        # Edges   
        #########################################################################################
        edge_channel = BRepBuilderAPI_MakeEdge(bend_start_3d, top_3d).Edge()
        
        # bend edge
        axis = gp_Ax2(bend_origin_3d, gp_Dir(0, 1, 0))
        circle = gp_Circ(axis, bend_radius)
        end_point = bend_end_3d
        if is_intersecting_bend: end_point = tandem_end_3d
        arc = GC_MakeArcOfCircle(circle, bend_start_3d, end_point, True).Value()
        edge_bend = BRepBuilderAPI_MakeEdge(arc).Edge()

        # extend bend if it doesn't exit the cylinder
        if not is_intersecting_bend: edge_extend_bend = BRepBuilderAPI_MakeEdge(bend_end_3d, tandem_end_3d).Edge()

        # top arc
        axis = gp_Ax2(top_arc_origin_3d, gp_Dir(0,1,0))
        circle = gp_Circ(axis, cylinder_radius)
        top_arc = GC_MakeArcOfCircle(circle, top_3d, tandem_end_3d, True).Value()
        edge_top_arc = BRepBuilderAPI_MakeEdge(top_arc).Edge()

        #########################################################################################
        # Wires   
        #########################################################################################

        if is_intersecting_bend: 
            wire_bend = BRepBuilderAPI_MakeWire(edge_bend).Wire()
            wire_profile = BRepBuilderAPI_MakeWire(edge_bend, edge_top_arc, edge_channel).Wire()
        else:
            wire_bend = BRepBuilderAPI_MakeWire(edge_bend, edge_extend_bend).Wire()
            wire_profile = BRepBuilderAPI_MakeWire(edge_bend, edge_extend_bend, edge_top_arc, edge_channel).Wire()

        #########################################################################################
        # Shapes
        #########################################################################################
        shape_channel = BRepPrimAPI_MakeCylinder(tandem_radius, max_height).Shape()

        bend_profile = BRepBuilderAPI_MakeWire(
            BRepBuilderAPI_MakeEdge(
                gp_Circ(
                    gp_Ax2(bend_start_3d, gp_Dir(0,0,1)),
                    tandem_radius)
            ).Edge()
        ).Wire()
        pipe = BRepFill_PipeShell(wire_bend)
        pipe.Add(bend_profile)
        pipe.Build()
        pipe.MakeSolid()
        shape_bend = pipe.Shape()

        shape_interior = make_symmetrical_shape(wire_profile, tandem_radius)

        # save values to self to use for stopper, if used
        self.bend_end = bend_end_3d
        self.bend_direction = gp_Dir(direction.X(), 0, direction.Y())
        self.tandem_end = tandem_end_3d

        return fuse_shapes([shape_channel, shape_interior, shape_bend])

    def __init__(self, *args, **kwargs):
        pass


def fuse_shapes(shapes: []):
    result = None
    for shape in shapes:
        if result is None:
            result = shape
            continue

        result = BRepAlgoAPI_Fuse(result, shape).Shape()

    return result


def intersection2d(curve1, curve2):
        intersection = Geom2dAPI_InterCurveCurve(curve1, curve2)

        result = gp_Pnt2d(0, -1000)
        if intersection.NbPoints() < 1:
            return None
        else:
            for i in range(1, intersection.NbPoints() + 1):
                point = intersection.Point(i)
                if point.Y() > result.Y():
                    result = point

        return result


def make_edge(p1: gp_Pnt, p2: gp_Pnt):
    return BRepBuilderAPI_MakeEdge(p1, p2).Edge()


def make_arc(start_point, end_point):
    p1 = gp_Pnt(start_point[0], start_point[1], start_point[2])
    p2 = gp_Pnt(end_point[0], end_point[1], end_point[2])
    direction = gp_Vec(0, 0, 1)
    arc = GC_MakeArcOfCircle(p1, direction, p2).Value()
    return BRepBuilderAPI_MakeEdge(arc).Edge()


def make_arc_from_points(origin_point, boundry_point, radius):
    p1 = gp_Pnt(origin_point[0], radius, origin_point[2])
    p2 = gp_Pnt(boundry_point[0], boundry_point[1], boundry_point[2])
    p3 = gp_Pnt(origin_point[0], -radius, origin_point[2])
    arc = GC_MakeArcOfCircle(p1, p2, p3).Value()
    return BRepBuilderAPI_MakeEdge(arc).Edge()


def make_point(point):
    p = gp_Pnt(point[0], point[1], point[2])
    return BRepPrimAPI_MakeSphere(p, 1.0).Shape()


def make_wire(edges: []):
    wire = BRepBuilderAPI_MakeWire()
    for edge in edges:
        wire.Add(edge)
    return wire.Wire()


def make_thru_shape(wires: []):
    shape = BRepOffsetAPI_ThruSections(True)
    for wire in wires:
        shape.AddWire(wire)
    return shape.Shape()


def make_cylinder(p1, p2, radius):
    p0 = gp_Pnt(p1[0], p1[1], p1[2])
    height = p2[2] - p1[2]
    return BRepPrimAPI_MakeCylinder(radius, height).Shape()


def make_symmetrical_shape(wire, distance):
    face = BRepBuilderAPI_MakeFace(wire).Face()
    prism = BRepPrimAPI_MakePrism(face, gp_Vec(0, distance, 0)).Shape()
    prism2 = BRepPrimAPI_MakePrism(face, gp_Vec(0, -distance, 0)).Shape()
    return BRepAlgoAPI_Fuse(prism, prism2).Shape()


def make_curved_pipe(start_point, arc, start_direction, radius):
    p1 = gp_Pnt(start_point[0], start_point[1], start_point[2])
    wire = BRepBuilderAPI_MakeWire(arc).Wire()
    direction = gp_Dir(start_direction[0],
                       start_direction[1], start_direction[2])
    axis = gp_Ax2(p1, direction)
    circle = gp_Circ(axis, radius)
    circle_edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    profile = BRepBuilderAPI_MakeWire(circle_edge).Wire()

    pipe = BRepFill_PipeShell(wire)
    pipe.Add(profile)
    pipe.Build()
    pipe.MakeSolid()
    return pipe.Shape()
    

def show_cylinder(
        cylinder_length: float = 160,
        cylinder_diameter: float =30) -> TopoDS_Shape:
    
    from OCC.Core.GC import GC_MakeSegment

    radius = cylinder_diameter / 2
    height = cylinder_length - radius

    top_point = gp_Pnt(0,0,cylinder_length)
    end_arc_point = gp_Pnt(radius, 0, height)
    bottom_point = gp_Pnt(radius, 0, 0)

    circle = gp_Circ(gp_Ax2(gp_Pnt(0,0, height), gp_Dir(0,1,0)), radius)
    curve = GC_MakeArcOfCircle(circle, top_point, end_arc_point, True)
    line = GC_MakeSegment(end_arc_point, bottom_point)

    edges = []
    edges.append(BRepBuilderAPI_MakeEdge(curve.Value()).Edge())
    edges.append(BRepBuilderAPI_MakeEdge(line.Value()).Edge())
    return make_wire(edges)


def to3d(point: gp_Pnt2d, y = 0.0) -> gp_Pnt:
    return gp_Pnt(point.X(), y, point.Y())


if __name__ == "__main__":
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    tandem = Tandem() # object to hold the tandem settings
    tandem.tandem_angle = 45.0  # manually change a setting

    display.DisplayColoredShape(tandem.generate_shape(), "BLUE")
    # generate a stopper
    #display.DisplayColoredShape(tandem.stopper_shape(), "ORANGE")

    # generate and show the tandem
    #display.DisplayShape(tandem.cylinder_offset_shape())
    start_display()
