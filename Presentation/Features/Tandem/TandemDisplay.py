from unittest import registerResult
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *

import Presentation.Features.Tandem.TandemFunctions as tandem
from Presentation.MainWindow.core import MainWindow
from Core.Models.Tandem import TandemModel



def init(window: MainWindow):
    """Called when the core class is initializing"""
    try:
        window.ui.btn_tandem_importToolModel.clicked.connect(lambda: tandem.load_tandem_model(window))
        window.ui.btn_tandem_clear.clicked.connect(lambda: tandem.clear_tandem_settings(window))
        window.ui.btn_tandem_add_update.clicked.connect(lambda: tandem.save_tandem(window))
        window.ui.listWidget_savedTandems.itemSelectionChanged.connect(lambda: tandem.set_tandem(window))
        tandem.load_tandems(window)
    except Exception as error_message:
        print(f"tandem display init failed: {error_message}")


## TANDEM
def view(window: MainWindow):
    # variables

    # set display
    window.display.default_drawer.SetFaceBoundaryDraw(True)  
    window.display._select_callbacks = []
    window.display.SetSelectionModeShape()
        
    update(window)


def update(window: MainWindow):
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
            
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.tandem.shape, color=color, material=Graphic3d_NOM_TRANSPARENT)
            
            # debugging
            import Application.BRep.Helper as brep
            color = Quantity_Color(0.0, 1.0, 0.0, Quantity_TOC_RGB)

            faces = brep.get_faces_axis(window.tandem.shape)

            for i, face in enumerate(faces):
                axis = face[1].Direction()
                location = face[2]
                result = axis.Z() < 0.0
                print(f" Result: {result} face {i}: axis X:{axis.X()} Y:{axis.Y()} Z:{axis.Z()} location X:{location.X()} Y:{location.Y()} Z:{location.Z()}")
                if result:
                    window.display.DisplayShape(shapes=face[0], color=color)

    except Exception as error_message:
        print(f"TandemView: Tandem load error: \n{error_message}")

    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)