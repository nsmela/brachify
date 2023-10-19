from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *

from Presentation.MainWindow.core import MainWindow
import Presentation.Features.Cylinder.CylinderFunctions as cylinder

## CYLINDER
def init(window: MainWindow):
    window.ui.cylinderDiameterSpinBox.valueChanged.connect(lambda: cylinder.setDiameter(window))
    window.ui.cylinderLengthSpinBox.valueChanged.connect(lambda: cylinder.setLength(window))
    window.ui.checkbox_cylinder_base.toggled.connect(lambda: cylinder.setBase(window))


def view(window: MainWindow):
    print("switched to cylinder view!")
    # variables

    # set display
    window.display._select_callbacks = []
    window.display.SetSelectionModeShape()
    window.display.default_drawer.SetFaceBoundaryDraw(True)

    update(window)

    # show left stacked widget menu
    window.ui.stackedWidget.setCurrentIndex(1)

def update(window: MainWindow) -> None:
    """When this is the active view, use this method to update the ui and 3d display view"""
    diameter = cylinder.DEFAULT_DIAMETER
    length = cylinder.DEFAULT_LENGTH
    expand_base = False

    if window.brachyCylinder is not None:
        diameter = window.brachyCylinder.diameter
        length = window.brachyCylinder.length
        expand_base = window.brachyCylinder.expand_base

    window.ui.cylinderDiameterSpinBox.blockSignals(True)
    window.ui.cylinderDiameterSpinBox.setValue(diameter)
    window.ui.cylinderDiameterSpinBox.blockSignals(False)

    window.ui.cylinderLengthSpinBox.blockSignals(True)
    window.ui.cylinderLengthSpinBox.setValue(length)
    window.ui.cylinderLengthSpinBox.blockSignals(False)

    window.ui.checkbox_cylinder_base.blockSignals(True)
    window.ui.checkbox_cylinder_base.setChecked(expand_base)
    window.ui.checkbox_cylinder_base.blockSignals(False)

    try:
        window.display.EraseAll()

        # cylinder shown
        if window.brachyCylinder is not None:
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            window.display.DisplayColoredShape(shapes=window.brachyCylinder.shape(), color=color)

    except Exception as error_message:
        print(f"CylinderView: Cylinder load error: \n{error_message}")

    try:
        # needles shown
        if window.needles is not None:
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.needles.shape(), material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"CylinderView: Channels load error: \n{error_message}")

    try:
        # tandem
        if window.tandem is not None:
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.tandem.shape(), color=color,
                                        material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"CylinderView: Tandem load error: \n{error_message}")

    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)