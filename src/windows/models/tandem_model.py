from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.gp import gp, gp_Vec
from OCC.Extend.ShapeFactory import translate_shp, rotate_shape

from PySide6.QtCore import QObject, Signal

from classes.app import get_app
from classes.logger import log
from classes.mesh.channel import NeedleChannel
from classes.mesh.helper import extend_bottom_face
from classes.mesh.tandem import generate_tandem
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
        self._base_shape = None
        self.update()

    def generate_tandem(self, 
        channel_diameter: float, tip_diameter: float,
        tip_thickness: float, tip_angle:float):
        log.debug(f"generating tandem")

        self.channel_diameter = channel_diameter
        self.tip_diameter = tip_diameter
        self.tip_thickness = tip_thickness
        self.tip_angle = tip_angle

        self._base_shape = generate_tandem(
            channel_diameter=self.channel_diameter,
            tip_diameter=self.tip_diameter,
            tip_thickness=self.tip_thickness,
            tip_angle=self.tip_angle,
            tip_height= TANDEM_TIP_HEIGHT_DEFAULT
        )
        self.update()

    def import_tandem(self, filepath: str):
        pass

    def set_tandem_channel(self, channel: NeedleChannel):
        log.debug(f"getting rotation from {channel}")
        self.rotation = channel.getRotation()
        self.update()

    def update(self):
        log.debug(f"updating")
        self.values_changed.emit()
        self.update_display()

    def update_display(self):
        log.debug(f"update display")
        if not self._base_shape:
            self.displaymodel.remove_shape(TANDEM_LABEL)
            return
        
        # TODO process shape
        shape = self.shape()
        if not shape: return

        shape_model = ShapeModel(
            label=TANDEM_LABEL, shape=shape, shape_type=ShapeTypes.TANDEM)
        
        get_app().window.displaymodel.add_shape(shape_model)

    def update_height_offset(self, height_offset:float):
        log.debug(f"updating tandem height offset to {height_offset}")
        self.height_offset = height_offset
        self.update()

    def shape(self):
        if not self._base_shape: return None
        log.debug(f"shape offsets being applied")
        # apply offsets
        offset = gp_Vec(0.0, 0.0, self.height_offset)
        rotation = self.rotation

        shape = rotate_shape(
            shape=self._base_shape, axis=gp.OZ(), angle=rotation)
        shape = translate_shp(shape, offset)
        #shape = extend_bottom_face(shape)

        return shape

    def __init__(self) -> None:
        super().__init__()
        self.base_shape = None  # base shape before extending due to height offset
        self.height_offset = 0.0
        self.rotation = 0.0

        # generated tandem settings
        self.channel_diameter = TANDEM_CHANNEL_DIAMETER_DEFAULT
        self.tip_diameter = TANDEM_TIP_DIAMETER_DEFAULT
        self.tip_thickness = TANDEM_TIP_THICKNESS_DEFAULT
        self.tip_angle = TANDEM_TIP_ANGLE_DEFAULT

        # references
        app = get_app()
        self.displaymodel = app.window.displaymodel

    @staticmethod
    def get_label(): return TANDEM_LABEL
