from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *
import Presentation.Features.NeedleChannels.NeedleFunctions as needleFunctions
from Presentation.MainWindow.display_functions import DisplayFunctions

from Presentation.MainWindow.core import MainWindow

import Application.BRep.Intersections as intersect


# def startView
# def updateView
# def endView


## NEEDLE CHANNELS


def init(window: MainWindow) -> None:
    window.ui.checkBox_hide_cylinder.stateChanged.connect(lambda: needleFunctions.setCylinderVisibility(window))
    window.ui.channelDiameterSpinBox.valueChanged.connect(lambda: needleFunctions.recalculate(window))
    window.ui.channelsListWidget.itemSelectionChanged.connect(
        lambda: needleFunctions.setActiveNeedleChannel(window, window.ui.channelsListWidget.currentRow()))
    window.ui.groupBox_5.setEnabled(False)
    window.ui.slider_needle_extension.valueChanged.connect(lambda: needleFunctions.setChannelOffset(window,
        window.ui.slider_needle_extension.value()))
    window.ui.btn_channel_disable.clicked.connect(lambda: needleFunctions.setNeedleDisabled(window))


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
    window.display.default_drawer.SetFaceBoundaryDraw(True)
    window.display.SetSelectionModeShape()
    window.display._select_callbacks = []
    window.display.register_select_callback(lambda shape, *args: selectNeedle(window, shape))

    diameter = window.ui.channelDiameterSpinBox.value()
    window.display_needles_list = []
    window.display_needles = None
    for needle in window.needles.channels:
        if needle.disabled:
            continue
        needle.shape = needleFunctions.generate_curved_channel(
            channel=needle,
            cylinder_offset=window.ui.cylinderLengthSpinBox.value() - 200.0,
            diameter=window.ui.channelDiameterSpinBox.value())
        window.display_needles_list.append(needle.shape)
        if window.display_needles:
            window.display_needles = BRepAlgoAPI_Fuse(window.display_needles, needle.shape).Shape()
        else:
            window.display_needles = needle.shape

    needleFunctions.set_tandem_offsets(window)

    update(window)


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
            # intersecting channels detection
            channels = []
            for channel in window.needles.channels:
                shape = channel.shape
                result = False
                for otherChannel in window.needles.channels:
                    if channel is otherChannel:
                        continue
                    result = intersect.are_colliding(channel.shape, otherChannel.shape)
                    if result:
                        break
                channels.append(
                    [channel.shape, result])  # TopoDS_Shape, bool (is it colliding with any other channels?)

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
