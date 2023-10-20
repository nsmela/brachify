from Core.Models.Cylinder import BrachyCylinder

from Presentation.MainWindow.core import MainWindow
import Presentation.Features.Cylinder.CylinderDisplay as cylinderDisplay
import Presentation.Features.NeedleChannels.NeedleFunctions as needleFunctions
import Presentation.Features.Tandem.TandemFunctions as tandemFunctions
from Core.Models.Cylinder import BrachyCylinder

DEFAULT_LENGTH = 160.0
DEFAULT_DIAMETER = 30.0


def setDiameter(window: MainWindow) -> None:
    if window.brachyCylinder is None:
        return

    window.brachyCylinder.diameter = window.ui.cylinderDiameterSpinBox.value()
    recalculate(window)


def setLength(window: MainWindow) -> None:
    if window.brachyCylinder is None:
        return

    window.brachyCylinder.length = window.ui.cylinderLengthSpinBox.value()
    window.brachyCylinder._shape = None  # next time the shape is needed, a new one will be generated

    # applying tandem height offset
    height_offset = window.brachyCylinder.length - DEFAULT_LENGTH
    tandemFunctions.applyOffsets(window, height_offset=height_offset)

    # applying needle channel height offset
    needleFunctions.applyOffsets(window, height_offset=height_offset)

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

    # applying offset to tandem
    height_offset = window.brachyCylinder.length - DEFAULT_LENGTH
    tandemFunctions.applyOffsets(window, height_offset=height_offset)

    # applying offset to needles

    # TODO update current view if cylinder view
