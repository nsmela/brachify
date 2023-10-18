from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *
import Presentation.Features.NeedleChannels.NeedleFunctions as needleFunctions
from Presentation.MainWindow.display_functions import DisplayFunctions

from Presentation.MainWindow.core import MainWindow

import Application.BRep.Intersections as intersect
import Application.BRep.Channel as channelHelper


# TODO list display variables as constants
# cylinder
# needle channel
# selected needle channel
# intersecting needle channel
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
        lambda: needleFunctions.setNeedleDisabled(window))

    # variables/settings
    window.channel_active_index = None  # which channel is selected?
    window.channel_hide_cylinder = False
    window.channel_diameter = 3.0


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
    window.ui.checkBox_hide_cylinder.setCheckState(window.channel_hide_cylinder)
    window.ui.checkBox_hide_cylinder.blockSignals(False)

    window.ui.channelsListWidget.blockSignals(True)
    index = -1
    if window.channel_active_index:
        index = window.needles_active_index
    window.ui.channelsListWidget.setCurrentRow(index)
    window.ui.channelsListWidget.blockSignals(False)

    window.ui.groupBox_5.blockSignals(True)
    enable_widget = window.channel_active_index is not None
    window.ui.groupBox_5.setEnabled(enable_widget)
    window.ui.groupBox_5.blockSignals(False)

    try:
        # TODO instead of clearing, try to find each shape and add it if it doesn't exist
        # TODO create a list of shapes within the display. If not in the display anynmore,
        #  remove them from display first then clear from list
        window.display.EraseAll()

        # cylinder shown
        if not window.isCylinderHidden and window.brachyCylinder.shape():
            window.display.DisplayShape(shapes=window.brachyCylinder.shape(), material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"Needle Display _cylinder error: \n {error_message}")

    try:
        # needles shown
        if window.needles is not None:
            # intersecting channels detection
            channels = []
            for channel in window.needles.channels:
                result = False
                for otherChannel in window.needles.channels:
                    if channel is otherChannel:
                        continue
                    result = intersect.are_colliding(channel.shape(), otherChannel.shape())
                    if result:
                        break
                channels.append(
                    [channel.shape(), result])  # TopoDS_Shape, bool (is it colliding with any other channels?)

            standard_color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            colliding_color = Quantity_Color(0.95, 0.1, 0.1, Quantity_TOC_RGB)
            selected_color = Quantity_Color(0.1, 0.4, 0.4, Quantity_TOC_RGB)
            for i, channel in enumerate(channels):
                if i == window.needles_active_index:
                    window.display.DisplayColoredShape(shapes=channel[0], color=selected_color)
                else:
                    color = standard_color
                    if channel[1]:
                        color = colliding_color
                    window.display.DisplayColoredShape(shapes=channel[0], color=color)

    except Exception as error_message:
        print(f"Needle Display _needles error: \n {error_message}")

    try:
        # tandem
        if window.tandem is not None:
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.tandem.tool_shape, color=color,
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

    if window.needles_active_index == index:
        return

    window.needles_active_index = index
    update(window)
