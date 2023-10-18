from Core.Models.Cylinder import BrachyCylinder
from Core.Models.DicomData import DicomData
from Presentation.MainWindow.core import MainWindow
import Presentation.Features.Cylinder.CylinderDisplay as cylinderDisplay
import Application.BRep.Cylinder as cyl


def setDiameter(window: MainWindow) -> None:
    if window.brachyCylinder is None:
        return

    window.brachyCylinder.diameter = window.ui.cylinderDiameterSpinBox.value()
    recalculate(window)


def setLength(window: MainWindow) -> None:
    if window.brachyCylinder is None:
        return

    window.brachyCylinder.length = window.ui.cylinderLengthSpinBox.value()
    window.brachyCylinder._shape = None

    window.tandem_height = window.brachyCylinder.length - 39.0
    if window.tandem is not None:
        window.tandem.setOffsets(window.tandem_height)

    window.channel_height_offset = window.brachyCylinder.length - 200.0
    if window.needles is not None:
        for i in range(len(window.needles.channels)):
            window.needles.channels[i].setOffset(window.channel_height_offset)

    cylinderDisplay.update(window)


def setBase(window: MainWindow) -> None:
    if window.brachyCylinder is None:
        return

    window.brachyCylinder.expand_base = window.ui.checkbox_cylinder_base.isChecked()
    recalculate(window)


def recalculate(window: MainWindow) -> None:
    """Called after the BrachyCylinder is changed"""
    print("Recalculating cylinder!")

    window.brachyCylinder.shape()
    cylinderDisplay.update(window)


def set_cylinder(window: MainWindow, cylinder: BrachyCylinder) -> None:
    window.brachyCylinder = cylinder
    window.brachyCylinder.shape()

    window.tandem_height = window.brachyCylinder.length - 39.0
    if window.tandem is not None:
        window.tandem.setOffsets(height=window.tandem_height)

    # TODO update current view if cylinder view
