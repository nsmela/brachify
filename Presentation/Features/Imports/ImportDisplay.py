from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *
from OCC.Core.TopoDS import TopoDS_Shape

from Presentation.MainWindow.core import MainWindow


## IMPORTS
def view(window: MainWindow):
    # variables

    # set page
    window.ui.stackedWidget.setCurrentIndex(0)
        
    # set display
        
    try:
        window.display._select_callbacks = []
        window.display.SetSelectionModeNeutral()
            
        window.display.EraseAll()

        # cylinder shown
        if window.brachyCylinder is not None:
            shape = window.display_cylinder
            color = Quantity_Color(0.25, 0.25, 0.25, Quantity_TOC_RGB)
            window.display.DisplayColoredShape(shapes=shape, color=color)

    except Exception as error_message:
        print(f"ImportView: Cylinder load error: {error_message}")

    try: 
        # needles shown
        if window.needles is not None:
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            window.display.DisplayColoredShape(shapes=window.display_needles, color=color)

    except Exception as error_message:
        print(f"ImportView: Channels load error: {error_message}")

    try: 
        # tandem
        if window.display_tandem is not None:
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayColoredShape(shapes=window.display_tandem, color=color)

    except Exception as error_message:
        print(f"ImportView: Tandem load error: {error_message}")

    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)