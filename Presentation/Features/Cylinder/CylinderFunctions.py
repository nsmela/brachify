from Presentation.MainWindow.core import MainWindow
import Presentation.Features.Cylinder.CylinderDisplay as cylinderDisplay


def setRadius(window: MainWindow) -> None:
    window.brachyCylinder.radius = window.ui.cylinderRadiusSpinBox.value() / 2 # diameter to radius
    recalculate(window)


def setLength(window: MainWindow) -> None:
    window.brachyCylinder.length = window.ui.cylinderLengthSpinBox.value()
    recalculate(window)
        

def setBase(window: MainWindow) -> None:
    window.brachyCylinder.expand_base = window.ui.checkbox_cylinder_base.isChecked()
    recalculate(window)


def recalculate(window: MainWindow) -> None:
    '''Called after the BrachyCylinder is changed'''
    print("Recalculating cylinder!")
    if window.isLocked:
        return
        
    window.display_cylinder = window.brachyCylinder.shape()
    cylinderDisplay.view(window)


def add_rs_file(window: MainWindow, filepath: str) -> None:
    import Application.Imports.import_dicom_structure as dicom
    window.brachyCylinder = dicom.read_cylinder_file(filepath=filepath)

    window.isLocked = True
    window.ui.cylinderRadiusSpinBox.setValue(window.brachyCylinder.radius * 2)
    window.ui.cylinderLengthSpinBox.setValue(window.brachyCylinder.length)
    window.ui.checkbox_cylinder_base.setChecked(window.brachyCylinder.expand_base)
    window.ui.lineedit_dicom_rs.setText(filepath)

    # global values for the cylinder offsets
    direction, length = window.brachyCylinder.getDirection()
    window.cylinder_offset_direction = direction
    window.cylinder_offset_length = length

    window.display_cylinder = window.brachyCylinder.shape()
    window.isLocked = False

    from Presentation.MainWindow.ui_functions import UIFunctions
    UIFunctions.setPage(window, UIFunctions.CYLINDER_VIEW)