from PySide6.QtCore import QObject, Signal

from classes.dicom.data import DicomData
from windows.models.shape_model import ShapeModel
from classes.mesh.channel import NeedleChannel

CHANNELS_LABEL = "applicator_"


class ChanelsModel(QObject):

    values_changed = Signal()

    def load_data(self, data: DicomData):
        pass

    def update_display(self):
        shapes = [ShapeModel(
            label=CHANNELS_LABEL,
            shape=shape
        ) for shape in self.channels]

        shape_model = ShapeModel(
            label=CHANNELS_LABEL, 
            shape=self.cylinder.shape())

        app = get_app()
        app.window.displaymodel.add_shapes(shape_model)

    def __init__(self):
        super().__init__()
        self.channels = []