from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp, gp_Vec
from OCC.Core.TopoDS import TopoDS_Compound
from OCC.Extend.ShapeFactory import translate_shp, rotate_shape

from PySide6.QtCore import QObject, Signal

from classes.app import get_app
from classes.dicom.data import DicomData
from classes.logger import log
from classes.mesh.channel import NeedleChannel
from windows.models.shape_model import ShapeModel, ShapeTypes

TANDEM_LABEL = "tandem"
# Defaults
TANDEM_CHANNEL_DIAMETER_DEFAULT = 4.0
TANDEM_TIP_DIAMETER_DEFAULT = 12.0
TANDEM_TIP_THICKNESS_DEFAULT = 10.0
TANDEM_TIP_ANGLE_DEFAULT = 45.0
TANDEM_TIP_HEIGHT_DEFAULT = 170.0


class TandemModel(QObject):

    values_changed = Signal()

    def clear_tandem(self):
        # remove tandem from the display
        pass

    def import_tandem(self):
        pass

    def generate_tandem(self):
        pass

    def set_tandem_channel(self, channel:NeedleChannel):
        # TODO: calculate rotation
        pass

    def set_tandem_settings(self, channel_diameter, tip_diameter, tip_thickness, tip_angle):
        pass

    def update(self):
        # TODO process chape
        # send shape to display
        pass

    def set_height_offset(self, height_offset:float):
        pass

    def __init__(self) -> None:
        super().__init__()
        self.base_shape = None  # base shape before extending due to height offset
        self.height_offset = 0.0
        self.rotation = 0.0

        self._base_shape = None  # file imported
        self._shape = None  # the shape used to cut from the model
        self.offset_height = 0.0  # translate offsets height
        self.rotation = 0.0  # rotation (0.0) along each axis xyz

        # variables to generate a tandem
        self.channel_diameter = TANDEM_CHANNEL_DIAMETER_DEFAULT
        self.tip_diameter = TANDEM_TIP_DIAMETER_DEFAULT
        self.tip_thickness = TANDEM_TIP_THICKNESS_DEFAULT
        self.tip_angle = TANDEM_TIP_ANGLE_DEFAULT
        self.tip_height = TANDEM_TIP_HEIGHT_DEFAULT

    def setOffsets(self, height: float = None, rotation: float = None) -> None:
        if height is not None:
            self.offset_height = height
        if rotation is not None:
            self.rotation = rotation

        self._shape = None
        self.shape()

    def shape(self):
        if self._shape is not None:
            return self._shape

        # apply offsets
        offset = gp_Vec(0.0, 0.0, self.offset_height)
        rotation = self.rotation

        if self._base_shape:
            self._shape = rotate_shape(
                shape=self._base_shape, axis=gp.OZ(), angle=rotation)
            self._shape = translate_shp(self._shape, offset)
            self._shape = extend_bottom_face(self._shape)
        return self._shape

    def import_shape(self, shape: TopoDS_Shape) -> None:
        self._base_shape = shape
        self._shape = None
        self.shape()

    def generate_shape(self):
        shape = generate_tandem(
            channel_diameter=self.channel_diameter,
            tip_diameter=self.tip_diameter,
            tip_thickness=self.tip_thickness,
            tip_angle=self.tip_angle,
            tip_height=self.tip_height + self.offset_height
        )
        rotation = self.rotation
        self._shape = rotate_shape(
            shape=shape, axis=gp.OZ(), angle=rotation)
        return self._shape

    @staticmethod
    def get_label(): return TANDEM_LABEL
