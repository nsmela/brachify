from Presentation.MainWindow.core import MainWindow
from Presentation.MainWindow.display_functions import DisplayFunctions


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
    DisplayFunctions.navigate_to_cylinder(window)