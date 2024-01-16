import math

from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge, BRepBuilderAPI_MakeWire, BRepBuilderAPI_MakeFace
from OCC.Core.BRepFill import BRepFill_PipeShell
from OCC.Core.BRepOffsetAPI import BRepOffsetAPI_ThruSections
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder, BRepPrimAPI_MakeSphere, BRepPrimAPI_MakePrism
from OCC.Core.GC import GC_MakeArcOfCircle
from OCC.Core.gp import *
from OCC.Core.TopoDS import TopoDS_Shape


# generates a custom tandem with inputed values
def generate_tandem(
        channel_diameter: float = 4.0,
        tip_diameter: float = 8.0,
        tip_thickness: float = 4.0,
        tip_angle=60.0,
        tip_height: float = 160.0) -> TopoDS_Shape:
    """Calculate the edges needs on a XZ plane where we pretend Z is Y"""
    # variables used
    tip_rads = math.radians(tip_angle)
    curve_offset = 15.0  # used for the curve
    channel_radius = channel_diameter / 2
    tip_radius = tip_diameter / 2

    # points
    p0 = [0, 0, 0]  # origin
    p1 = [0, 0, tip_height]  # where the tip begins

    # creating a curved edge, so the next point needs to be [cos(angle), 0, sin(angle)]
    x = curve_offset - (math.cos(tip_rads) * curve_offset)
    z = math.sin(tip_rads) * curve_offset  # curve offset sets the length
    p2 = [x, 0, z + tip_height]

    # tip continues along where the curve ends
    # the angle at the end of the curve
    angle_rads = math.radians(90 - tip_angle)
    x = math.cos(angle_rads)
    z = math.sin(angle_rads)
    vec = gp_Vec(x, 0, z) * tip_thickness
    p3 = [p2[0] + vec.X(), 0, p2[2] + vec.Z()]

    # lines to be used later
    line1 = Line(p1=p2, p2=p3)
    line2 = line1.get_perpindicular_line(p2)
    line3 = line1.get_perpindicular_line(p3)

    # tip's base
    p4 = line2.get_point_distance_from(p2, -tip_radius)  # pos x end
    p6 = line2.get_point_from_x(-channel_radius)  # neg x end
    p5 = line2.get_point_distance_from(p6, -tip_radius)

    edges = []
    edges.append(make_arc_from_points(p2, p4, tip_radius))
    edges.append(make_edge([p2[0], -tip_radius, p2[2]],
                 [p5[0], -tip_radius, p5[2]]))
    edges.append(make_arc_from_points(p5, p6, tip_radius))
    edges.append(make_edge([p2[0], tip_radius, p2[2]],
                 [p5[0], tip_radius, p5[2]]))

    wires = []
    wires.append(make_wire(edges))

    # tip's end
    p7 = line3.get_point_distance_from(p3, -tip_radius)  # pos x boundry
    p9 = line3.get_point_from_x(-channel_radius)  # neg x boundry
    p8 = line3.get_point_distance_from(p9, -tip_radius)

    edges = []
    edges.append(make_arc_from_points(p3, p7, tip_radius))
    edges.append(make_edge([p3[0], -tip_radius, p3[2]],
                 [p8[0], -tip_radius, p8[2]]))
    edges.append(make_arc_from_points(p8, p9, tip_radius))
    edges.append(make_edge([p3[0], tip_radius, p3[2]],
                 [p8[0], tip_radius, p8[2]]))
    wires.append(make_wire(edges))

    # base filling in
    edges = []
    p_height = line2.get_point_from_x(0)
    edges.append(make_edge(p1, p_height))
    edges.append(make_edge(p_height, p2))
    edges.append(make_arc(p1, p2))

    wire = make_wire(edges)

    # shapes
    shapes = []
    shapes.append(make_cylinder(p0, p6, channel_radius))
    shapes.append(make_symmetrical_shape(wire, channel_radius))
    shapes.append(make_curved_pipe(
        p1, make_arc(p1, p2), [0, 0, 1], channel_radius))
    shapes.append(make_thru_shape(wires))

    return fuse_shapes(shapes)


def make_edge(p1, p2):
    p1 = gp_Pnt(p1[0], p1[1], p1[2])
    p2 = gp_Pnt(p2[0], p2[1], p2[2])
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


def fuse_shapes(shapes: []):
    result = None
    for shape in shapes:
        if result is None:
            result = shape
            continue

        result = BRepAlgoAPI_Fuse(result, shape).Shape()

    return result


class Line:
    def __init__(self, *, p1=None, p2=None, m: float = None, b: float = None):
        self.slope = m or Line._get_slope(p1, p2)
        self.y_intercept = b or Line._get_y_intercept(self.slope, p1)

    def _get_slope(p1, p2):
        """m = y2 - y1 / x2 - x1"""
        rise = p2[2] - p1[2]
        run = p2[0] - p1[0]
        return rise / run

    def _get_y_intercept(slope: float, p1: []):
        return p1[2] - (slope * p1[0])

    def get_perpindicular_line(self, p1: []):
        slope = self.slope
        m = -1 / slope
        b = Line._get_y_intercept(m, p1)
        return Line(m=m, b=b)

    def get_point_from_x(self, x: float) -> []:
        m = self.slope
        b = self.y_intercept
        return [x, 0, m * x + b]

    def get_point_from_y(self, y: float) -> []:
        m = self.slope
        b = self.y_intercept
        return [(y - b) / m, 0, y]

    def get_point_distance_from(self, p1: [], distance: float) -> []:
        value = distance / math.sqrt(1 + self.slope**2)
        if distance > 0:
            x = p1[0] + value
        else:
            x = p1[0] - value
        return self.get_point_from_x(x)


def generate_new_tandem(
        cylinder_height: float = 160.0,
        tandem_height: float = 129.0,  # default
        tandem_diameter: float = 8.0,
        tandem_angle: float = 60.0,
        bend_radius: float = 15.0,
        tandem_length: float = 8.0) -> TopoDS_Shape:

    # variables
    height_offset = 10.0  # how much futher above cylinder this tandem shows

    tandem_rads = math.radians( tandem_angle)
    tandem_radius = tandem_diameter / 2

    p0 = [0, 0, 0]  # origin
    p1 = [0, 0, tandem_height]  # start of bend
    p2 = [0, 0, tandem_height + bend_radius]  # end of bend radius straight up
    pTop = [0, 0, cylinder_height + height_offset]  # where tandem ends

    # calculate bend
    x = (1 - math.cos(tandem_rads)) * bend_radius
    z = math.sin(tandem_rads) * bend_radius

    # determine direction to find the arc's end point
    arc_point = [x, 0, z + tandem_height]

    # continuing the direction
    angle_rads = math.radians(90 - tandem_angle)
    x = math.cos(angle_rads)
    z = math.sin(angle_rads)
    vector = gp_Vec(x, 0 , z) * tandem_length
    end_point = [arc_point[0] + vector.X(), 0, arc_point[2] + vector.Z()]

    # top arc
    # does tandem length line start within circle for cylinder top?
    # distance from pTop - cylinder radius will be less than cylinder radius
    
    # if so, find intersect
    # if not, find intersect with bend radius circle
    # https://dev.opencascade.org/doc/overview/html/occt_user_guides__modeling_algos.html
    # https://liuxinwin_admin.gitee.io/pythonocc-docs/OCC.Geom2dAPI.html#OCC.Geom2dAPI.Geom2dAPI_InterCurveCurve
    # https://github.com/tpaviot/pythonocc-demos/blob/4c5af9e6b6a0fcd1885b3c44325e2a890d80136a/examples/core_modeling_sprocket.py#L131C78-L131C78


    # make the lines
    edges = []
    edges.append(make_edge(p0, p1))
    edges.append(make_edge(p1, p2))
    
    # arc
    def arc(origin, radius, start_point, end_point):
        p0 = gp_Pnt(origin[0], origin[1], origin[2])
        p1 = gp_Pnt(start_point[0], start_point[1], start_point[2])
        p2 = gp_Pnt(end_point[0], end_point[1], end_point[2])
        circle = gp_Circ(gp_Ax2(p0, gp_Dir(0, 1, 0)), radius)
        arc = GC_MakeArcOfCircle(circle, p1, p2, False).Value()
        return BRepBuilderAPI_MakeEdge(arc).Edge()

    bend_point = [bend_radius, 0, tandem_height]

    edges.append(arc(bend_point, bend_radius, p1, arc_point))
    #edges.append(make_edge(arc_point, p1))
    #edges.append(make_edge(p1, bend_point))
    #edges.append(make_edge(bend_point, arc_point))
    edges.append(make_edge(arc_point, end_point))
    print(edges)

    wire = make_wire(edges)

    return wire
    # generating the shape by collecting all small shapes
    # and boolean_addition

    def cylinder(origin, end, radius):
        p0 = gp_Pnt(origin[0], origin[1], origin[2])
        p1 = gp_Pnt(end[0], end[1], end[2])
        direction = p1- p0
        axis = gp_Ax2(p0, direction)
        return BRepPrimAPI_MakeCylinder()

    shapes = []
    shapes.append(make_cylinder(p0, p1, tandem_radius))
    # axis = gp_Ax2(gp_Pnt(p1[0], p1[1], p1[2]), gp_Dir(0,0,1))
    # tip_cyl = BRepPrimAPI_MakeCylinder(axis, tip_radius, tip_thickness)
    # shapes.append(tip_cyl.Shape())
    shapes.append(make_symmetrical_shape(wire, tandem_radius))

    return fuse_shapes(shapes)


def tandem_from_2d(        
        cylinder_height: float = 160.0,
        cylinder_diamter: float = 15,
        tandem_height: float = 129.0,  # default
        tandem_diameter: float = 8.0,
        tandem_angle: float = 60.0,
        bend_radius: float = 35.0,
        tandem_length: float = 8.0) -> TopoDS_Shape:

    from OCC.Core.Geom2d import Geom2d_Circle, Geom2d_Line, Geom2d_TrimmedCurve
    from OCC.Core.Geom2dAPI import Geom2dAPI_InterCurveCurve

    height_offset = 10.0
    max_height = cylinder_height + height_offset
    tandem_radius = tandem_diameter / 2
    cylinder_radius = (cylinder_diamter + height_offset) / 2

    origin = gp_Pnt2d(0,0)
    bend_start = gp_Pnt2d(0, tandem_height)

    # bend
    bend_origin = gp_Pnt2d(bend_radius, tandem_height)
    bend_rads = math.radians(180-tandem_angle)
    x = math.cos(bend_rads)
    y = math.sin(bend_rads)
    bend_direction = gp_Dir2d(x, y)
    bend_line = gp_Lin2d(bend_origin, bend_direction)
    bend_circle = gp_Circ2d(gp_Ax22d(bend_origin, bend_direction), bend_radius)

    line_curve = Geom2d_Line(bend_line)
    bend_curve = Geom2d_Circle(bend_circle)
    intersection = Geom2dAPI_InterCurveCurve(bend_curve, line_curve)

    if intersection.NbPoints() > 1:
        bend_end = gp_Pnt2d(0, -100)
        for i in range(1, intersection.NbPoints() + 1):
            point = intersection.Point(i)
            print(f"Point: {point.X()}, {point.Y()}")
            if point.Y() > bend_end.Y():
                bend_end = point

    new_line = bend_line.Rotated(bend_end, math.radians(90))
    direction = new_line.Direction()
    bend_vector = gp_Vec2d(direction) * tandem_length * -1
    tandem_end = gp_Pnt2d(bend_end.X() + bend_vector.X(), bend_end.Y() + bend_vector.Y())
    tandem_top = gp_Pnt2d(0, max_height)

    # top arc
    top_circle_origin = gp_Pnt2d(0, max_height - cylinder_radius)
    top_circle = gp_Circ2d(gp_Ax2d(top_circle_origin, gp_Dir2d(0, 1)), cylinder_radius)
    top_curve = Geom2d_Circle(top_circle)
    tandem_final_line = Geom2d_Line(bend_end, direction)
    intersection = Geom2dAPI_InterCurveCurve(top_curve, tandem_final_line)

    if intersection.NbPoints() > 1:
        top_tandem_point = gp_Pnt2d(0, -100)
        for i in range(1, intersection.NbPoints() + 1):
            point = intersection.Point(i)
            print(f"Point: {point.X()}, {point.Y()}")
            if top_tandem_point.Y() < point.Y():
                top_tandem_point = point

    distance = top_circle_origin.Distance(bend_end)
    print(f" is bend end in range? Distance of {distance} vs {cylinder_diamter} : {distance < cylinder_diamter}")

    # calculate intersection of tandem output and cylinder top curve


    print(f"Results:\n\n" \
          f"Origin: {origin.X()},{origin.Y()}\n" \
          f"Bend Start: {bend_start.X()},{bend_start.Y()}\n" \
          f"Bend End: {bend_end.X()},{bend_end.Y()}\n" \
          f"Tandem End: {tandem_end.X()},{tandem_end.Y()}"  \
          f"Top of model: {tandem_top.X()},{tandem_top.Y()}")

    # wire
    p0 = gp_Pnt(origin.X(),     0,     origin.Y())
    p1 = gp_Pnt(bend_start.X(), 0,     bend_start.Y())
    p2 = gp_Pnt(bend_end.X(),   0,     bend_end.Y())
    p3 = gp_Pnt(tandem_end.X(), 0,     tandem_end.Y())
    p4 = gp_Pnt(tandem_top.X(), 0,     tandem_top.Y())
    p5 = gp_Pnt(top_tandem_point.X(), 0, top_tandem_point.Y())

    edges = []
    def arc_generate(arc_start, arc_end, radius):
        p0 = gp_Pnt(arc_start.X(), 0, arc_start.Y())
        p1 = gp_Pnt(arc_end.X(), 0, arc_end.Y())
        o = gp_Pnt(arc_start.X() + radius, 0, arc_start.Y())

        axis = gp_Ax2(o, gp_Dir(0,1,0))
        circle = gp_Circ(axis, radius)
        return GC_MakeArcOfCircle(circle, p0, p1, True).Value()
    
    edges.append(BRepBuilderAPI_MakeEdge(arc_generate(bend_start, bend_end, bend_radius)).Edge())
    edges.append(BRepBuilderAPI_MakeEdge(p2, p5).Edge())
    edges.append(BRepBuilderAPI_MakeEdge(p1, p4).Edge())

    # top arc
    o = gp_Pnt(p4.X(), p4.Y(), p4.Z() - cylinder_radius)
    axis = gp_Ax2(o, gp_Dir(0,1,0))
    circle = gp_Circ(axis, cylinder_radius)
    arc = GC_MakeArcOfCircle(circle, p4, p5, True).Value()
    edges.append(BRepBuilderAPI_MakeEdge(arc).Edge())

    #extra edges for display
    edges.append(BRepBuilderAPI_MakeEdge(p0, p1).Edge())

    wire = make_wire(edges)

    return wire
    shapes = []
    shapes.append(BRepPrimAPI_MakeCylinder(tandem_radius, max_height).Shape())

    curve_axis = gp_Ax2(p1, gp_Dir(0,0,1))
    curve_circle = gp_Circ(curve_axis, tandem_radius)
    arc_edge = GC_MakeArcOfCircle(curve_circle, p1, p2, True).Value()
    bend_wire = BRepBuilderAPI_MakeWire(
        BRepBuilderAPI_MakeEdge(arc_edge).Edge(),
        BRepBuilderAPI_MakeEdge(p2, p3).Edge()).Wire()
    direction = gp_Dir(0,0,1)
    axis = gp_Ax2(p1, direction)
    circle = gp_Circ(axis, tandem_radius)
    circle_edge = BRepBuilderAPI_MakeEdge(circle).Edge()
    profile = BRepBuilderAPI_MakeWire(circle_edge).Wire()

    pipe = BRepFill_PipeShell(bend_wire)
    pipe.Add(profile)
    pipe.Build()
    pipe.MakeSolid()

    shapes.append(pipe.Shape())
    shapes.append(make_symmetrical_shape(wire, tandem_radius))

    return fuse_shapes(shapes)

def show_cylinder(
        cylinder_length: float = 160,
        cylinder_diameter: float =30) -> TopoDS_Shape:
    
    from OCC.Core.GC import GC_MakeSegment

    radius = cylinder_diameter / 2
    height = cylinder_length - radius

    top_point = gp_Pnt(0,0,cylinder_length)
    curve_point = gp_Pnt(radius/2, 0, height + (radius/2))
    end_arc_point = gp_Pnt(radius, 0, height)
    bottom_point = gp_Pnt(radius, 0, 0)

    circle = gp_Circ(gp_Ax2(gp_Pnt(0,0, height), gp_Dir(0,1,0)), radius)
    curve = GC_MakeArcOfCircle(circle, top_point, end_arc_point, True)
    line = GC_MakeSegment(end_arc_point, bottom_point)

    edges = []
    edges.append(BRepBuilderAPI_MakeEdge(curve.Value()).Edge())
    edges.append(BRepBuilderAPI_MakeEdge(line.Value()).Edge())
    return make_wire(edges)

if __name__ == "__main__":
    from OCC.Display.SimpleGui import init_display

    display, start_display, add_menu, add_function_to_menu = init_display()

    tandem_angle = 30.0

    display.DisplayColoredShape(tandem_from_2d(
        tandem_angle=tandem_angle), "BLUE")
    # generate a stopper

    # generate and show the tandem
    display.DisplayShape(show_cylinder())
    start_display()
