from PySide6.QtCore import QObject, Signal
from classes.dicom.data import DicomData


class DicomModel(QObject):

    values_changed = Signal(DicomData)

    def __init__(self):
        super().__init__()
        self.data = DicomData()

    def update(self, data: DicomData):
        self.data = data
        self.values_changed.emit(data)
