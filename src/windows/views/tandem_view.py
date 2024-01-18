from PySide6.QtWidgets import QWidget, QFileDialog

from classes.app import get_app
from classes.logger import log
from windows.models.shape_model import ShapeTypes
from windows.ui.tandem_view_ui import Ui_Tandem_View
from windows.views.custom_view import display_action, CustomView

materials = {
    ShapeTypes.CYLINDER: {"rgb": [0.8, 0.8, 0.8], "transparent": True},
    ShapeTypes.CHANNEL: {"rgb": [0.8, 0.8, 0.8], "transparent": True},
    ShapeTypes.TANDEM: {"rgb": [0.2, 0.55, 0.55], "transparent": False},
    ShapeTypes.SELECTED: {"rgb": [0.2, 0.8, 0.55], "transparent": True}
}


class TandemView(CustomView):

    @display_action
    def action_clear_tandem(self):
        log.debug(f"action: clearing tandem")
        self.tandemmodel.clear_tandem()

    @display_action
    def action_set_tandem(self):
        log.debug(f"action: generate a tandem")

        self.tandemmodel.set_tandem(
            channel_diameter=self.ui.sp_channel_diameter.value(),
            tip_diameter=self.ui.sp_tip_diameter.value(),
            tip_thickness=self.ui.sp_tip_thickness.value(),
            tip_angle=self.ui.sp_tip_angle.value()
        )

    @display_action
    def action_import_tandem(self):
        log.debug(f"action: import a tandem")
        # file dialog to choose file
        filename = QFileDialog.getOpenFileName(self, 'Select Tandem Tool Model', "", "Supported files (*.stl *.3mf *.obj *.stp *.step)")[0]

        if not filename:  # no folder selected?
            log.info("no valid filename selected for importing")
            return

        log.info(f"file {filename} has been selected")
        
        self.tandemmodel.import_tandem(filename)
        self.update_settings()

    @display_action
    def action_set_import_offset(self, offset):
        self.tandemmodel.set_import_height_offset(offset)

    def on_close(self):
        log.debug(f"on view close")

    @display_action
    def on_open(self):
        log.debug(f"on view open")

        displaymodel = get_app().window.displaymodel
        displaymodel.set_materials(materials)
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

        filepath = self.tandemmodel.filepath
        self.ui.label_5.setText(f"Model filepath:\n{filepath}")

    def __init__(self):
        super().__init__()
        self.ui = Ui_Tandem_View()  # the converted python file from the ui file
        self.ui.setupUi(self)
        self.tandemmodel = get_app().window.tandemmodel

        # signals and slots
        self.ui.btn_apply.pressed.connect(self.action_set_tandem)
        self.ui.btn_clear_generate.pressed.connect(self.action_clear_tandem)
        self.ui.btn_import.pressed.connect(self.action_import_tandem)
        self.ui.btn_clear_import.pressed.connect(self.action_clear_tandem)
        self.ui.sb_height_offset.valueChanged.connect(self.action_set_import_offset)

        self.update_settings()
