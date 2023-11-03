from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *

import Presentation.Features.Tandem.TandemFunctions as tandem
from Presentation.MainWindow.core import MainWindow
import Application.Tandem.Models as tandemModel

TANDEM_COLOUR = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)

def init(window: MainWindow):
    """Called when the core class is initializing"""
    try:
        window.ui.btn_tandem_importToolModel.clicked.connect(lambda: tandem.load_tandem_model(window))
        window.ui.btn_tandem_clear.clicked.connect(lambda: tandem.clear_tandem_settings(window))
        window.ui.btn_tandem_add_update.clicked.connect(lambda: tandem.save_tandem(window))
        window.ui.listWidget_savedTandems.itemSelectionChanged.connect(lambda: tandem.set_tandem(window))
        window.ui.btn_tandem_apply.clicked.connect(lambda: tandem.create_tandem(window))
        tandem.load_tandems(window)
        
        window.tandem_height_offset = tandem.tandem_height
        window.tandem_rotation_offset = tandem.DEFAULT_ROTATION

        window.tandem = tandemModel.Tandem()
    
    except Exception as error_message:
        print(f"tandem display init failed: {error_message}")


## TANDEM
def view(window: MainWindow):
    print("Tandem view!")
    # variables

    # set display
    window.display.default_drawer.SetFaceBoundaryDraw(True)  
    window.display._select_callbacks = []
    window.display.SetSelectionModeShape()
    
    # setting custom tandem settings
    tandem = window.tandem
    if tandem is None: tandem = tandemModel.Tandem()

    # ui elements here do not have a signal, so no need to pause them while adding values
    window.ui.tandem_spinbox_channel_diameter.setValue(tandem.channel_diameter)
    window.ui.tandem_spinbox_tip_diameter.setValue(tandem.tip_diameter)
    window.ui.tandem_spinbox_tip_angle.setValue(tandem.tip_angle)
    window.ui.tandem_spinbox_tip_thickness.setValue(tandem.tip_thickness)

    update(window)


def update(window: MainWindow):
    try:
        window.display.EraseAll()

        # cylinder shown
        if window.brachyCylinder is not None:
            window.display.DisplayShape(shapes=window.brachyCylinder.shape(), material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"TandemView: Cylinder load error: \n{error_message}")

    try: 
        # needles shown
        if window.needles is not None:
            window.display.DisplayShape(shapes=window.needles.shape(), material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"TandemView: Needles load error: \n{error_message}")

    try: 
        # tandem
        if window.tandem is not None:
            window.display.DisplayShape(shapes=window.tandem.shape(), color=TANDEM_COLOUR, material=Graphic3d_NOM_TRANSPARENT)
            
            # debugging
            import Application.BRep.Helper as brep
            color = Quantity_Color(0.0, 1.0, 0.0, Quantity_TOC_RGB)

            faces = brep.get_faces_axis(window.tandem.shape())

            for i, face in enumerate(faces):
                axis = face[1].Direction()
                location = face[2]
                result = axis.Z() < 0.0
                if result:
                    window.display.DisplayShape(shapes=face[0], color=color)

    except Exception as error_message:
        print(f"TandemView: Tandem load error: \n{error_message}")

    try:
        tandem = window.tandem.generate_shape()
        window.display.DisplayShape(tandem)
    except Exception as error_message:
        print(f"TandemView: Custom tandem error: \n{error_message}")


    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)