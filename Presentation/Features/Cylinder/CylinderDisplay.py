from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *
from OCC.Core.TopoDS import TopoDS_Shape

from Presentation.MainWindow.core import MainWindow


## CYLINDER
def navigate_to_cylinder(window: MainWindow):
    print("switched to cylinder view!")
    # variables

    # set page
    window.ui.stackedWidget.setCurrentIndex(1)
        
    # set display
    window.display._select_callbacks = []
    window.display.SetSelectionModeShape()
        
    try:
        window.display.EraseAll()

        # cylinder shown
        if window.brachyCylinder is not None:
            shape = window.display_cylinder
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            window.display.DisplayColoredShape(shapes=shape, color=color)

    except Exception as error_message:
        print(f"CylinderView: Cylinder load error: \n{error_message}")

    try: 
        # needles shown
        if window.needles is not None:
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.display_needles, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"CylinderView: Channels load error: \n{error_message}")

    try: 
        # tandem
        if window.display_tandem:
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.display_tandem, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"CylinderView: Tandem load error: \n{error_message}")

    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)
