from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *

import Presentation.Features.Tandem.TandemFunctions as tandem
from Presentation.MainWindow.core import MainWindow
from Core.Models.Tandem import TandemModel



def init(window: MainWindow):
    try:
        window.ui.btn_tandem_importDisplayModel.clicked.connect(lambda: tandem.load_tandem_display_model(window))
        window.ui.btn_tandem_importToolModel.clicked.connect(lambda: tandem.load_tandem_tool_model(window))
        window.ui.btn_tandem_clear.clicked.connect(lambda: tandem.clear_tandem_settings(window))
        window.ui.btn_tandem_add_update.clicked.connect(lambda: tandem.save_tandem(window))
        window.ui.listWidget_savedTandems.itemSelectionChanged.connect( 
            lambda: tandem.set_tandem(window, window.ui.listWidget_savedTandems.currentRow()))
        tandem.load_tandems(window)
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
        
    update(window)


def update(window:MainWindow):
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
            
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.tandem.tool_shape, color=color, material=Graphic3d_NOM_TRANSPARENT)
            
            # debugging
            import Application.BRep.Helper as brep
            color = Quantity_Color(0.0, 1.0, 0.0, Quantity_TOC_RGB)

            faces = brep.get_faces(window.tandem.tool_shape)
            print(faces)
            for face in faces:
                if brep.face_is_plane(face[0]) and face[1] < 25.0 and face[1] > 15.0:
                    window.display.DisplayShape(shapes=face[0], color=color)

    except Exception as error_message:
        print(f"TandemView: Tandem load error: \n{error_message}")

    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)