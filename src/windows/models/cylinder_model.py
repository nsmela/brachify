from PySide6.QtCore import QObject, Signal

from classes.app import get_app
from classes.dicom.data import DicomData
from classes.mesh.cylinder import BrachyCylinder, get_brachy_cylinder
from windows.models.shape_model import ShapeModel

CYLINDER_LABEL = "cylinder"


class CylinderModel(QObject):

    values_changed = Signal(BrachyCylinder)

    def update(self, cylinder: BrachyCylinder):
        self.cylinder = cylinder
        self.values_changed.emit(cylinder)
        self.update_display()

    def load_data(self, data: DicomData):
        self.cylinder = get_brachy_cylinder(data)
        self.values_changed.emit(self.cylinder)
        self.update_display()

    def update_display(self):
        shape_model = ShapeModel(
            label=CYLINDER_LABEL, 
            shape=self.cylinder.shape())

        app = get_app()
        app.window.displaymodel.add_shape(shape_model)

    def __init__(self):
        super().__init__()
        self.cylinder = None

    @staticmethod
    def get_label(): return CYLINDER_LABEL
