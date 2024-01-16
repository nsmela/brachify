from OCC.Core.Bisector import Bisector_BisecCC
from OCC.Display.SimpleGui import init_display
from OCC.Core.GCE2d import GCE2d_MakeLine, GCE2d_MakeCircle
from OCC.Core.Geom2dAPI import Geom2dAPI_InterCurveCurve
from OCC.Core.Geom2d import Geom2d_Circle, Geom2d_Line
from OCC.Core.GccAna import GccAna_Lin2dBisec, GccAna_CircLin2dBisec, GccAna_Pnt2dBisec
from OCC.Core.gp import gp_Lin2d, gp_Pnt2d, gp_Dir2d, gp_Circ2d, gp_Ax22d, gp_Pnt

from OCC.Extend.ShapeFactory import make_vertex, make_edge2d

# start gui
display, start_display, add_menu, add_function_to_menu = init_display()


def bisect_lineline(event=None):
    display.EraseAll()
    li1 = gp_Lin2d(gp_Pnt2d(), gp_Dir2d(1, 0))
    li2 = gp_Lin2d(gp_Pnt2d(), gp_Dir2d(0, 1))

    bi = GccAna_Lin2dBisec(li1, li2)
    bi_li1 = bi.ThisSolution(1)
    bi_li2 = bi.ThisSolution(2)

    for i in [li1, li2]:
        display.DisplayShape(make_edge2d(i))
    for i in [bi_li1, bi_li2]:
        display.DisplayColoredShape(make_edge2d(i), "BLUE")
    display.FitAll()


def bisect_linecircle(event=None):
    display.EraseAll()
    ci1 = gp_Circ2d(gp_Ax22d(), 100)
    li1 = gp_Lin2d(gp_Pnt2d(-8, 0), gp_Dir2d(10, 0))

    circle_curve = Geom2d_Circle(ci1)
    line_curve = Geom2d_Line(li1)
    intersection = Geom2dAPI_InterCurveCurve(circle_curve, line_curve)
    if intersection.NbPoints() > 1:
        for i in range(1, intersection.NbPoints() + 1):
            point = intersection.Point(i)
            print(f"Point: {point.X()}, {point.Y()}")

    display.DisplayColoredShape(make_edge2d(ci1), "RED")
    display.DisplayColoredShape(make_edge2d(li1), "BLUE")
    display.FitAll()
    return
    bi = GccAna_CircLin2dBisec(ci1, li1)
    if not bi.IsDone():
        raise AssertionError("Bisec is not Done")
    bisec = bi.ThisSolution(1)
    pb = bisec.Parabola()
    display.DisplayColoredShape([make_edge2d(ci1), make_edge2d(li1)], "GREEN")
    display.DisplayColoredShape(make_edge2d(pb), "BLUE")
    display.FitAll()


def bisect_pnt(event=None):
    display.EraseAll()
    p1 = gp_Pnt2d(1, 0.5)
    p2 = gp_Pnt2d(0, 1e5)
    bi = GccAna_Pnt2dBisec(p1, p2)
    bisec = bi.ThisSolution()
    # enum GccInt_Lin, GccInt_Cir, GccInt_Ell, GccInt_Par, GccInt_Hpr, GccInt_Pnt
    p1_ = make_vertex(gp_Pnt(p1.X(), p1.Y(), 0))
    p2_ = make_vertex(gp_Pnt(p2.X(), p2.Y(), 0))
    display.DisplayShape([p1_, p2_])
    display.DisplayColoredShape(make_edge2d(bisec), "BLUE")
    display.FitAll()


def bisect_crvcrv(event=None):
    display.EraseAll()
    ax = gp_Ax22d(gp_Pnt2d(), gp_Dir2d(1, 0), gp_Dir2d(0, -1))
    circ = gp_Circ2d(ax, 5)
    crv1 = GCE2d_MakeCircle(circ).Value()
    edg1 = make_edge2d(crv1, -1.0, 1.0)
    display.DisplayColoredShape(edg1, "BLUE")

    p1 = gp_Pnt2d(-10, 0)
    p2 = gp_Pnt2d(-10, 10)
    crv2 = GCE2d_MakeLine(p1, p2).Value()
    edg2 = make_edge2d(crv2, -10.0, 10.0)
    display.DisplayColoredShape(edg2, "GREEN")

    bi = Bisector_BisecCC(crv1, crv2, 50, -5, gp_Pnt2d(0, 0))
    crv_bi = bi.Curve(1)
    edg3 = make_edge2d(crv_bi, -1.0, 1.0)
    display.DisplayColoredShape(edg3, "RED")
    display.FitAll()


if __name__ == "__main__":
    add_menu("bisector")
    add_function_to_menu("bisector", bisect_lineline)
    add_function_to_menu("bisector", bisect_linecircle)
    add_function_to_menu("bisector", bisect_pnt)
    add_function_to_menu("bisector", bisect_crvcrv)
    start_display()
