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

    window.brachyCylinder.setDiameter(window.ui.cylinderDiameterSpinBox.value())
    cylinderDisplay.update(window)


def setLength(window: MainWindow) -> None:
    if window.brachyCylinder is None:
        return

    window.brachyCylinder.setLength(window.ui.cylinderLengthSpinBox.value())

    # applying tandem height offset
    height_offset = window.brachyCylinder.length - DEFAULT_LENGTH
    tandemFunctions.applyOffsets(window, height_offset=height_offset)

    # applying needle channel height offset
    needleFunctions.applyOffsets(window, height_offset=height_offset)

    cylinderDisplay.update(window)


def setBase(window: MainWindow) -> None:
    if window.brachyCylinder is None:
        return

    window.brachyCylinder.enableBase(window.ui.checkbox_cylinder_base.isChecked())
    cylinderDisplay.update(window)


def set_cylinder(window: MainWindow, cylinder: BrachyCylinder) -> None:
    cylinder.setLength(DEFAULT_LENGTH)
    window.brachyCylinder = cylinder

    height_offset = window.brachyCylinder.length - DEFAULT_LENGTH
    # applying offset to tandem
    tandemFunctions.applyOffsets(window, height_offset=height_offset)
    # applying offset to needles
    needleFunctions.applyOffsets(window, height_offset=height_offset)

    # TODO update current view if cylinder view
