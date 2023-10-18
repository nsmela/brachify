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
    # TODO: change offset for needle channels
    # TODO change offset for Tandem
    recalculate(window)


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
    # TODO update current view if cylinder view
