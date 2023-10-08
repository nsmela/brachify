from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *

import Presentation.Features.Tandem.TandemFunctions as tandem
from Presentation.MainWindow.core import MainWindow
from Core.Models.Tandem import Tandem 



def init(window: MainWindow):
    try:
        window.ui.btn_tandem_importDisplayModel.clicked.connect(lambda: tandem.load_tandem_display_model(window))
        window.ui.btn_tandem_importToolModel.clicked.connect(lambda: tandem.load_tandem_tool_model(window))
        window.ui.btn_tandem_clear.clicked.connect(lambda: tandem.clear_tandem_settings(window))
    except:
        pass


## TANDEM
def view(window: MainWindow):
    # variables

    # set page
    window.ui.stackedWidget.setCurrentIndex(3)
        
    # set display
    window.display._select_callbacks = []
    window.display.SetSelectionModeShape()
        
    try:
        window.display.EraseAll()

        # cylinder shown
        if window.brachyCylinder is not None:
            shape = window.display_cylinder
            window.display.DisplayShape(shapes=shape, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"TandemView: Cylinder load error: \n{error_message}")

    try: 
        # needles shown
        if window.needles is not None:
            window.display.DisplayShape(shapes=window.display_needles, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"TandemView: Needles load error: \n{error_message}")

    try: 
        # tandem
        if window.tandem is not None:
            color = Quantity_Color(0.2, 0.2, 0.55, Quantity_TOC_RGB)
            window.display.DisplayColoredShape(shapes=window.tandem.shape, color=color)

    except Exception as error_message:
        print(f"TandemView: Tandem load error: \n{error_message}")

    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)

def update(window:MainWindow, tandem: Tandem):
    pass