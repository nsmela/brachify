from PySide6.QtWidgets import QWidget

from classes.app import get_app
from classes.logger import log
from classes.dicom.data import DicomData
from windows.ui.tandem_view_ui import Ui_Tandem_View
from windows.models.shape_model import ShapeTypes

colours = {
    ShapeTypes.CYLINDER: [1.0, 1.0, 1.0],
    ShapeTypes.CHANNEL: [1.0, 1.0, 1.0],
    ShapeTypes.TANDEM: [0.2, 0.55, 0.55],
    ShapeTypes.SELECTED: [0.5, 0.5, 0.2]}


class TandemView(QWidget):

    def action_clear_tandem(self):
        log.debug(f"action: clearing tandem")
        self.tandemmodel.clear_tandem()

    def action_generate_tandem(self):
        log.debug(f"action: generate a tandem")
        self.tandemmodel.generate_tandem(
            channel_diameter=self.ui.sp_channel_diameter.value(),
            tip_diameter=self.ui.sp_tip_diameter.value(),
            tip_thickness=self.ui.sp_tip_thickness.value(),
            tip_angle=self.ui.sp_tip_angle.value()
        )

    def action_import_tandem(self):
        log.debug(f"action: import a tandem")
        # file dialog to choose file

    def on_view_close(self):
        log.debug(f"on view close")

        displaymodel = get_app().window.displaymodel
        displaymodel.set_transparent(False)

    def on_view_open(self):
        log.debug(f"on view open")

        displaymodel = get_app().window.displaymodel
        displaymodel.set_shape_colour(colours)
        displaymodel.set_transparent(True)
        self.tandemmodel.update_display()

        self.update_settings()

    def update_settings(self):
        log.debug(f"updating settings")
        channel_diameter = self.tandemmodel.channel_diameter
        self.ui.sp_channel_diameter.setValue(channel_diameter)

        tip_diameter = self.tandemmodel.tip_diameter
        self.ui.sp_tip_diameter.setValue(tip_diameter)

        tip_thickness = self.tandemmodel.tip_thickness
        self.ui.sp_tip_thickness.setValue(tip_thickness)

        tip_angle = self.tandemmodel.tip_angle
        self.ui.sp_tip_angle.setValue(tip_angle)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Tandem_View()  # the converted python file from the ui file
        self.ui.setupUi(self)
        self.tandemmodel = get_app().window.tandemmodel

        # signals and slots
        self.ui.btn_apply.pressed.connect(self.action_generate_tandem)
        self.ui.btn_clear_generate.pressed.connect(self.action_clear_tandem)
        self.ui.btn_clear_import.pressed.connect(self.action_clear_tandem)

        self.update_settings()
