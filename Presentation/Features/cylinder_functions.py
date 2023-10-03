from Presentation.MainWindow.core import MainWindow
from Presentation.MainWindow.display_functions import DisplayFunctions

class CylinderFunctions(MainWindow):
    def setRadius(self) -> None:
        self.brachyCylinder.radius = self.ui.cylinderRadiusSpinBox.value() / 2 # diameter to radius
        CylinderFunctions.__recalculateCylinder__(self)

    def setLength(self) -> None:
        self.brachyCylinder.length = self.ui.cylinderLengthSpinBox.value()
        CylinderFunctions.__recalculateCylinder__(self)
        
    def setBase(self) -> None:
        self.brachyCylinder.expand_base = self.ui.checkbox_cylinder_base.isChecked()
        CylinderFunctions.__recalculateCylinder__(self)

    def __recalculateCylinder__(self):
        '''Called after the BrachyCylinder is changed'''
        self.display_cylinder = self.brachyCylinder.shape()
        DisplayFunctions.navigate_to_cylinder(self)