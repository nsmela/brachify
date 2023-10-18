from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.AIS import AIS_Shape

from Presentation.MainWindow.core import MainWindow


## EXPORT
def init(window: MainWindow):
    window.display_export = None


def view(window: MainWindow):
    # set display
    window.display._select_callbacks = []
    window.display.SetSelectionModeNeutral()

    update(window)

def update(window: MainWindow):
    shape = TopoDS_Shape()

    try:
        window.display.EraseAll()

        # cylinder shown
        if window.brachyCylinder:
            shape = window.brachyCylinder.shape()

    except Exception as error_message:
        print(error_message)

    try:
        # needles shown
        if window.needles:
            shape = BRepAlgoAPI_Cut(shape, window.needles.shape()).Shape()

    except Exception as error_message:
        print(error_message)

    try:
        # tandem
        if window.tandem:
            shape = BRepAlgoAPI_Cut(shape, window.tandem.shape()).Shape()

    except Exception as error_message:
        print(error_message)

    try:
        color = Quantity_Color(0.8, 0.1, 0.1, Quantity_TOC_RGB)

        window.display.default_drawer.SetFaceBoundaryDraw(False)

        window.display.DisplayShape(shapes=shape, color=color, material=Graphic3d_NOM_TRANSPARENT)

        window.display.FitAll()
        window.display_export = shape
    except Exception as error_message:
        print(error_message)