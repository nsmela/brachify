from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

from Application.BRep.Channel import generate_curved_channel
from Presentation.MainWindow.core import MainWindow
import Application.BRep.Helper as helper
import Presentation.Features.NeedleChannels.NeedlesDisplay as needlesDisplay
from Presentation.Features.NeedleChannels.needlesModel import NeedlesModel

from Application.NeedleChannels.Models import NeedleChannel

import numpy as np

'''
Manages the functions and display values for the Needles and the Channel View
self.display_needles: all needle channels fused as a single model
self.display_needle_list: a list of the needle channels
self.needles_active_index: the current active needle channel
'''


def set_channels(window: MainWindow, channels: list[NeedleChannel]) -> None:
    # offset each point
    if window.brachyCylinder:
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
    window.ui.channelsListWidget.clear()
    for needle in window.needles.channels:
        window.ui.channelsListWidget.addItem(needle.channelId)

    diameter = 3.00

    # update the spin box without triggering the change event
    window.ui.channelDiameterSpinBox.blockSignals(True)
    window.ui.channelDiameterSpinBox.setValue(diameter)
    window.ui.channelDiameterSpinBox.blockSignals(False)



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


def setNeedleDisabled(window: MainWindow):
    index = window.channel_active_index
    if index < 0:
        return

    channel = window.needles.channels[window.channel_active_index]
    channel.disabled = not channel.disabled
    needlesDisplay.update(window)


def setChannelsDiameter(window: MainWindow, diameter: float = 3.0) -> None:
    if window.needles is None:
        return

    window.channel_diameter = diameter

    for channel in window.needles.channels:
        channel.setDiameter(window.channel_diameter)

    needlesDisplay.update(window)


def set_tandem_offsets(window: MainWindow) -> None:
    tandem_channel = window.needles.channels[0]

    # position
    window.tandem_offset_position = tandem_channel.points[-1]

    # rotation
    window.tandem_offset_rotation = tandem_channel.getRotation()
    print(f"Rotation calculated: {window.tandem_offset_rotation}")



