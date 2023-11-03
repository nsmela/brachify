from OCC.Extend.ShapeFactory import translate_shp, rotate_shape
from OCC.Core.gp import gp, gp_Vec
from OCC.Core.TopoDS import TopoDS_Shape

from src.Core.Models.Tandem import TandemModel
from src.Application.BRep.Helper import extend_bottom_face
from src.Application.BRep.Tandem import generate_tandem


class Tandem(TandemModel):
    def __init__(self) -> None:
        super().__init__()
        self._base_shape = None  # file imported
        self._shape = None  # the shape used to cut from the model
        self.offset_height = 0.0  # translate offsets height
        self.rotation = 0.0  # rotation (0.0) along each axis xyz

        # variables to generate a tandem
        self.channel_diameter = 4.0
        self.tip_diameter = 8.0
        self.tip_thickness = 4.0
        self.tip_angle = 45.0
        self.tip_height = 160.0

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
            tip_angle= self.tip_angle,
            tip_height= self.tip_height
        )
        rotation = self.rotation
        self._shape = rotate_shape(
            shape=shape, axis=gp.OZ(), angle=rotation)
        return self._shape
