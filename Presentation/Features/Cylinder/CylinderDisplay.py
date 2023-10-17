from OCC.Core.Quantity import Quantity_Color, Quantity_TOC_RGB
from OCC.Core.Graphic3d import *

from Presentation.MainWindow.core import MainWindow


## CYLINDER
def view(window: MainWindow):
    print("switched to cylinder view!")
    # variables

    # set display
    window.display._select_callbacks = []
    window.display.SetSelectionModeShape()
    window.display.default_drawer.SetFaceBoundaryDraw(True)

    update(window)


def update(window: MainWindow) -> None:
    """When this is the active view, use this method to update the ui and 3d display view"""
    window.ui.cylinderRadiusSpinBox.blockSignals(True)
    window.ui.cylinderRadiusSpinBox.setValue(window.brachyCylinder.radius * 2)
    window.ui.cylinderRadiusSpinBox.blockSignals(False)

    window.ui.cylinderLengthSpinBox.blockSignals(True)
    window.ui.cylinderLengthSpinBox.setValue(window.brachyCylinder.length)
    window.ui.cylinderLengthSpinBox.blockSignals(False)

    window.ui.checkbox_cylinder_base.blockSignals(True)
    window.ui.checkbox_cylinder_base.setChecked(window.brachyCylinder.expand_base)
    window.ui.checkbox_cylinder_base.blockSignals(False)

    try:
        window.display.EraseAll()

        # cylinder shown
        if window.brachyCylinder is not None:
            shape = window.display_cylinder
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            window.display.DisplayColoredShape(shapes=shape, color=color)

    except Exception as error_message:
        print(f"CylinderView: Cylinder load error: \n{error_message}")

    try:
        # needles shown
        if window.needles is not None:
            color = Quantity_Color(0.35, 0.2, 0.35, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.display_needles, material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"CylinderView: Channels load error: \n{error_message}")

    try:
        # tandem
        if window.tandem is not None:
            color = Quantity_Color(0.2, 0.55, 0.55, Quantity_TOC_RGB)
            window.display.DisplayShape(shapes=window.tandem.tool_shape, color=color,
                                        material=Graphic3d_NOM_TRANSPARENT)

    except Exception as error_message:
        print(f"CylinderView: Tandem load error: \n{error_message}")

    try:
        window.display.FitAll()
    except Exception as error_message:
        print(error_message)