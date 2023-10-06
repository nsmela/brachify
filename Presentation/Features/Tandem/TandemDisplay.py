from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *
import Presentation.Features.Tandem.TandemFunctions as tandem
from Presentation.MainWindow.display_functions import DisplayFunctions

from Presentation.MainWindow.core import MainWindow


## TANDEM
def navigate_to_tandem(window: MainWindow):
    # variables

    # set page
    window.ui.stackedWidget.setCurrentIndex(3)
        
    # set display
    window.display._select_callbacks = []
    window.display.SetSelectionModeShape()
        
    try:
        window.display.EraseAll()

        # cylinder shown
        if window.brachyCylinder:
            shape = window.display_cylinder
            window.display.DisplayShape(shapes=shape, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(error_message)

    try: 
        # needles shown
        if window.needles:
            window.display.DisplayShape(shapes=window.display_needles, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(error_message)

    try: 
        # tandem
        if window.display_tandem:
            color = Quantity_Color(0.2, 0.2, 0.55, Quantity_TOC_RGB)
            window.display.DisplayColoredShape(shapes=window.display_tandem, color=color)

    except Exception as error_message:
        print(error_message)

    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)
