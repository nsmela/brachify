from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *
import Presentation.Features.NeedleChannels.NeedleFunctions as needles
from Presentation.MainWindow.display_functions import DisplayFunctions

from Presentation.MainWindow.core import MainWindow


# def startView
# def updateView
# def endView


## NEEDLE CHANNELS
def view(window: MainWindow) -> None:
    # variables
    window.ui.channelsListWidget.setCurrentRow(window.needles_active_index)

    # set page
    if window.needles_active_index >= 0:
        window.ui.groupBox_5.setEnabled(True) 
        channel = window.needles.channels[window.needles_active_index]
        window.ui.slider_needle_extension.setValue(channel.curve_downwards)
    else:
        window.ui.groupBox_5.setEnabled(False) 
        window.ui.slider_needle_extension.setValue(0)
            
    window.ui.stackedWidget.setCurrentIndex(2)
        
    # set display
    window.display.SetSelectionModeShape()
    window.display._select_callbacks = []
    window.display.register_select_callback(lambda shape, *args: selectNeedle(window, shape))

    try:
        window.display.EraseAll()

        # cylinder shown
        if not window.isCylinderHidden and window.brachyCylinder:
            shape = window.display_cylinder
            window.display.DisplayShape(shapes=shape, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(error_message)

    try: 
        # needles shown
        if window.needles:
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            for needle in window.display_needles_list:
                window.display.DisplayColoredShape(shapes=needle, color=color)

            if window.needles_active_index >= 0:
                color = Quantity_Color(0.1, 0.4, 0.4, Quantity_TOC_RGB)
                shape = window.display_needles_list[window.needles_active_index]
                window.display.DisplayColoredShape(shapes=shape, color=color)
                    
    except Exception as error_message:
        print(error_message)

    try: 
        # tandem
         if window.tandem is not None:
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.tandem.tool_shape, color=color, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(error_message)

    try:
        window.display.FitAll()
        window.display.Repaint()
    except Exception as error_message:
        print(error_message)


def update(window: MainWindow):
    print("NeedlesDisplay: update!!")
    # update view UI
    if window.needles_active_index >= 0:
        window.ui.groupBox_5.setEnabled(True) 
        channel = window.needles.channels[window.needles_active_index]
        window.ui.slider_needle_extension.setValue(channel.curve_downwards)
    else:
        window.ui.groupBox_5.setEnabled(False) 
        window.ui.slider_needle_extension.setValue(0)
    
    try:
        window.display.EraseAll()

        # cylinder shown
        if not window.isCylinderHidden and window.brachyCylinder:
            shape = window.display_cylinder
            window.display.DisplayShape(shapes=shape, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"Needle Display _cylinder error: \n {error_message}")
        
    try: 
        # needles shown
        if window.needles is not None:
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            selected_color = Quantity_Color(0.1, 0.4, 0.4, Quantity_TOC_RGB)
            for i, channel in enumerate(window.needles.channels):
                if i == window.needles_active_index:
                    window.display.DisplayColoredShape(shapes=channel.shape, color=selected_color)
                else:
                    window.display.DisplayColoredShape(shapes=channel.shape, color=color)
                    
    except Exception as error_message:
        print(f"Needle Display _needles error: \n {error_message}")
        
    try: 
        # tandem
         if window.tandem is not None:
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.tandem.tools_shape, color=color, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(error_message)
        
    try:
        window.display.FitAll()
        window.display.Repaint()
    except Exception as error_message:
        print(error_message)


def selectNeedle(window: MainWindow, shapes):
    index = -1
    if len(shapes) > 0:
        index  = needles.get_clicked_needle_index(window, shapes[0])
    window.needles_active_index = index
    view(window)