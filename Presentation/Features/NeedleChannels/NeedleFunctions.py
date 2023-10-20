from Presentation.MainWindow.core import MainWindow
import Application.BRep.Helper as helper
import Presentation.Features.NeedleChannels.NeedlesDisplay as needlesDisplay
from Presentation.Features.NeedleChannels.needlesModel import NeedlesModel
import Presentation.Features.Tandem.TandemFunctions as tandemFunctions
from Application.NeedleChannels.Models import NeedleChannel
import Application.BRep.Intersections as intersect

from OCC.Core.TopoDS import TopoDS_Shape

import numpy as np

'''
Manages the functions and display values for the Needles and the Channel View
self.display_needles: all needle channels fused as a single model
self.display_needle_list: a list of the needle channels
self.needles_active_index: the current active needle channel
'''

DEFAULT_DIAMETER = 3.0
DEFAULT_HEIGHT = 0.0


def set_channels(window: MainWindow, channels: list[NeedleChannel]) -> None:
    # offset each point
    if window.brachyCylinder:
        # use the brachy cylinder to offset the points
        z_up = np.array([0, 0, 1])  # z axis reference, the direction we want the cylinder and needles to go
        tip = np.array(window.brachyCylinder.tip)
        base = np.array(window.brachyCylinder.base)
        cyl_vec = tip - base  # the cylinder's original vector
        cyl_length = np.linalg.norm(cyl_vec)
        offset_vector = np.array([0, 0, - cyl_length])  # normalized direction from tip to base

        for i, c in enumerate(channels):
            new_points = np.array(c.rawPoints)
            new_points = np.array(new_points) - base
            new_points = helper.rotate_points(new_points, cyl_vec, z_up)
            new_points = new_points - offset_vector
            channels[i].points = list(list(points) for points in new_points)
    window.needles = NeedlesModel(channels=channels)

    # offset
    for i in range(len(window.needles.channels)):
        window.needles.channels[i].setOffset(window.channel_height_offset)

    # channel 0 is the tandem needle channel
    set_tandem_needle(window, 0)
    setNeedleDisabled(window, 0)

    # list of needles in widget
    window.ui.channelsListWidget.clear()
    for needle in window.needles.channels:
        window.ui.channelsListWidget.addItem(needle.channelId)

    diameter = 3.00

    # update the spin box without triggering the change event
    window.ui.channelDiameterSpinBox.blockSignals(True)
    window.ui.channelDiameterSpinBox.setValue(diameter)
    window.ui.channelDiameterSpinBox.blockSignals(False)

    # propagate the channels to be displayed and if they're colliding
    window.channels = checkIntersecting(window)

def setActiveNeedleChannel(window: MainWindow, index: int = -1) -> None:
    if window.channel_active_index == index:
        return

    window.channel_active_index = index
    if len(window.ui.channelsListWidget.selectedIndexes()) < 1 or \
            index != window.ui.channelsListWidget.selectedIndexes()[0].row():
        window.ui.channelsListWidget.setCurrentRow(index)
    needlesDisplay.update(window)


def setCylinderVisibility(window: MainWindow) -> None:
    window.isCylinderHidden = window.ui.checkBox_hide_cylinder.isChecked()
    needlesDisplay.update(window)


def get_clicked_needle_index(window: MainWindow, shape) -> int:
    for i, needle in enumerate(window.needles.channels):
        if shape == needle.shape():
            return i

    return -1


def setNeedleDisabled(window: MainWindow, index: int) -> None:
    if index < 0 or index >= len(window.needles.channels):
        return

    channel = window.needles.channels[index]
    window.needles.channels[index].disabled = not channel.disabled
    window.needles.clearShape()
    window.channels = checkIntersecting(window)

    needlesDisplay.update(window)


def setChannelsDiameter(window: MainWindow, diameter: float = 3.0) -> None:
    if window.needles is None:
        return

    window.channel_diameter = diameter

    for channel in window.needles.channels:
        channel.setDiameter(window.channel_diameter)

    window.channels = checkIntersecting(window)

    needlesDisplay.update(window)


def set_tandem_needle(window: MainWindow, index: int) -> None:
    tandem_channel = window.needles.channels[index]

    # position
    # window.tandem_offset_position = tandem_channel.points[-1]  # last point is the height

    # rotation
    rotation = tandem_channel.getRotation()
    print(f"Rotation calculated: {rotation}")

    tandemFunctions.applyOffsets(window, rotation=rotation)


def applyOffsets(window, height_offset: float) -> None:
    window.channel_height_offset = height_offset

    if window.needles is None or len(window.needles.channels) < 1:
        return None

    #for i in range(len(window.needles.channels)):
       # window.needles.channels[i].setOffset(window.channel_height_offset)

    [channel.setOffset(window.channel_height_offset) for channel in window.needles.channels]
    window.needles.clearShape()


def checkIntersecting(window: MainWindow) -> None:
    channels = None

    # needles shown
    if window.needles is not None:
        # intersecting channels detection
        # shapes to check if they collide with each the needle channel
        otherShapes = [channel.shape() for channel in window.needles.channels if not channel.disabled]
        if window.tandem is not None:
            otherShapes.append(window.tandem.shape())

        # intersection testing returns an array of [shape, bool] where bool is if anything intersects it
        for channel in window.needles.channels:
            if channel.disabled:
                channel.isIntersecting = False
                continue
            result = False  # is the shape intersecting something?
            shape = channel.shape()  # shape to test
            for otherShape in otherShapes:
                if shape is otherShape:
                    continue  # skip if its own shape
                result = intersect.are_colliding(shape, otherShape)
                if result:
                    break
            channel.isIntersecting = result  # TopoDS_Shape, bool (is it colliding with any other channels?)
