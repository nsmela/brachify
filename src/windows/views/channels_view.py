from PySide6.QtWidgets import QWidget

from classes.app import get_app
from classes.logger import log
from classes.dicom.data import DicomData
from windows.ui.channels_view_ui import Ui_Channels_View
from windows.models.channels_model import ChannelsModel
from windows.models.cylinder_model import CylinderModel
from windows.models.shape_model import ShapeTypes

colours = {
    ShapeTypes.CYLINDER: [1.0, 1.0, 1.0],
    ShapeTypes.CHANNEL: [0.2, 0.55, 0.55],
    ShapeTypes.TANDEM: [1.0, 1.0, 1.0]}


class ChannelsView(QWidget):

    def action_set_diameter(self):
        diameter = self.ui.spinbox_diameter.value()
        log.debug(f"setting channel diameters to: {diameter}")
        get_app().window.channelsmodel.set_diameter(diameter)

    def action_set_view(self, view_index: int):
        if view_index != 2:
            return  # this view is page 1, exit if not this view

        log.debug(f"switching to channels view")
        get_app().window.displaymodel.set_shape_colour(colours)

    def action_update_settings(self):
        log.debug(f"updating channels view")
        
        model = get_app().window.channelsmodel
        
    def __init__(self):
        super().__init__()
        self.ui = Ui_Channels_View()  # the converted python file from the ui file
        self.ui.setupUi(self)

        # signals and slots
        self.ui.btn_apply_diameter.pressed.connect(self.action_set_diameter)

        app = get_app()
        app.signals.viewChanged.connect(self.action_set_view)

        window = app.window
        window.channelsmodel.values_changed.connect(self.action_update_settings)

        self.action_update_settings()
