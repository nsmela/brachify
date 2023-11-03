from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *

import src.Presentation.Features.NeedleChannels.NeedleFunctions as needleFunctions
from src.Presentation.MainWindow.core import MainWindow

from PySide6.QtWidgets import QCheckBox

# TODO list display colours as constants
CYLINDER_COLOUR = Quantity_Color(0.0, 0.0, 0.0, Quantity_TOC_RGB)
TANDEM_COLOUR = Quantity_Color(0.0, 0.0, 0.0, Quantity_TOC_RGB)
CHANNEL_COLOUR_STANDARD = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
CHANNEL_COLOUR_ACTIVE = Quantity_Color(0.2, 0.95, 0.55, Quantity_TOC_RGB)
CHANNEL_COLOUR_COLLIDING = Quantity_Color(0.95, 0.1, 0.1, Quantity_TOC_RGB)
CHANNEL_COLOUR_DISABLED = Quantity_Color(0.05, 0.05, 0.05, Quantity_TOC_RGB)
# close proximity needle channel
# outside cylinder needle channel


## NEEDLE CHANNELS
def init(window: MainWindow) -> None:
    print("Needles Display: init!")
    window.ui.checkBox_hide_cylinder.stateChanged.connect(
        lambda: needleFunctions.setCylinderVisibility(window))
    window.ui.channelDiameterSpinBox.valueChanged.connect(
        lambda: needleFunctions.setChannelsDiameter(window, window.ui.channelDiameterSpinBox.value()))
    window.ui.channelsListWidget.itemSelectionChanged.connect(
        lambda: needleFunctions.setActiveNeedleChannel(window, window.ui.channelsListWidget.currentRow()))
    window.ui.btn_channel_disable.clicked.connect(
        lambda: needleFunctions.setNeedleDisabled(window, window.channel_active_index))

    # variables/settings
    window.channel_active_index = None  # which channel is selected?
    window.channel_tandem_index = None
    window.channel_hide_cylinder = False
    window.channel_diameter = needleFunctions.DEFAULT_DIAMETER
    window.channel_height_offset = needleFunctions.DEFAULT_HEIGHT
    window.channels = []

def view(window: MainWindow) -> None:
    print("Needles Display: view!")
    # set display
    window.display.default_drawer.SetFaceBoundaryDraw(True)
    window.display.SetSelectionModeShape()
    window.display._select_callbacks = []
    window.display.register_select_callback(lambda shape, *args: selectNeedle(window, shape))

    update(window)

    # show left stacked widget menu
    window.ui.stackedWidget.setCurrentIndex(2)


def update(window: MainWindow):
    print("Needles Display: update!")

    # set stacked widget objects
    window.ui.channelDiameterSpinBox.blockSignals(True)
    window.ui.channelDiameterSpinBox.setValue(window.channel_diameter)
    window.ui.channelDiameterSpinBox.blockSignals(False)

    window.ui.checkBox_hide_cylinder.blockSignals(True)
    #window.ui.checkBox_hide_cylinder.setCheckState(window.channel_hide_cylinder)
    window.ui.checkBox_hide_cylinder.blockSignals(False)

    window.ui.channelsListWidget.blockSignals(True)
    index = -1
    if window.channel_active_index is not None:
        index = window.channel_active_index
    window.ui.channelsListWidget.setCurrentRow(index)
    window.ui.channelsListWidget.blockSignals(False)

    window.ui.groupBox_5.blockSignals(True)
    enable_widget = window.channel_active_index is not None
    label = "Disable"
    if window.channel_active_index is not None \
        and window.needles.channels[window.channel_active_index].disabled:
        label = "Enable"
    window.ui.groupBox_5.setEnabled(enable_widget)
    window.ui.btn_channel_disable.setText(label)
    window.ui.groupBox_5.blockSignals(False)

    try:
        # TODO instead of clearing, try to find each shape and add it if it doesn't exist
        # TODO create a list of shapes within the display. If not in the display anynmore,
        #  remove them from display first then clear from list
        window.display.EraseAll()

        # cylinder shown
        if not window.isCylinderHidden and window.brachyCylinder.shape():
            window.display.DisplayShape(shapes=window.brachyCylinder.shape(), color=CYLINDER_COLOUR,
                            material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"Needle Display _cylinder error: \n {error_message}")

    try:
        # needles shown
        if window.needles is not None:
            channels = window.needles.channels

            for i, channel in enumerate(channels):
                if i == window.channel_tandem_index \
                        and window.tandem is not None:
                    continue

                color = CHANNEL_COLOUR_STANDARD
                if i == window.channel_active_index:
                    color=CHANNEL_COLOUR_ACTIVE
                elif channel.isIntersecting:
                    color = CHANNEL_COLOUR_COLLIDING
                elif channel.disabled:
                    color = CHANNEL_COLOUR_DISABLED
                window.display.DisplayShape(shapes=channel.shape(), color=color,
                                            material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"Needle Display _needles error: \n {error_message}")

    try:
        # tandem
        if window.tandem is not None:
            window.display.DisplayShape(shapes=window.tandem.shape(), color=TANDEM_COLOUR,
                                        material=Graphic3d_NOM_TRANSPARENT)

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
        index = needleFunctions.get_clicked_needle_index(window, shapes[0])

    if window.channel_active_index == index:
        return

    window.channel_active_index = index
    update(window)
