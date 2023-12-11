from PySide6.QtCore import QObject, Signal

from OCC.Core.TopoDS import TopoDS_Compound

from classes.app import get_app
from classes.dicom.data import DicomData
from classes.logger import log
from classes.mesh.channel import NeedleChannel
from windows.models.shape_model import ShapeModel, ShapeTypes

CHANNELS_LABEL = "tandem"


class TandemModel(QObject):
    pass