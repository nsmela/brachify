from PySide6.QtWidgets import QWidget

from classes.app import get_app
from classes.logger import log
from classes.dicom.data import DicomData
from windows.ui.tandem_view_ui import Ui_Tandem_View
from windows.models.shape_model import ShapeTypes

colours = {
    ShapeTypes.CYLINDER: [1.0, 1.0, 1.0],
    ShapeTypes.CHANNEL: [1.0, 1.0, 1.0],
    ShapeTypes.TANDEM: [0.5, 0.55, 0.55],
    ShapeTypes.SELECTED: [0.5, 0.5, 0.2]}


class TandemView(QWidget):

    def action_set_view(self, view_index: int):
        log.debug(f"action: set tandem view")
        if view_index != 3:
            self.on_view_close()
            return  # this view is page 3, exit if not this view

        if not self.is_active:
            log.debug(f"switching to tandem view")
            self.on_view_open()

    def action_update_settings(self):
        pass

    def on_view_close(self):
        if not self.is_active: return
        log.debug(f"on view close")

        self.is_active = False

        displaymodel = get_app().window.displaymodel
        displaymodel.set_transparent(False)

    def on_view_open(self):
        log.debug(f"on view open")
        self.is_active = True

        displaymodel = get_app().window.displaymodel
        displaymodel.set_shape_colour(colours)
        displaymodel.set_transparent(True)

        self.action_update_settings()

    def __init__(self):
        super().__init__()
        self.ui = Ui_Tandem_View()  # the converted python file from the ui file
        self.ui.setupUi(self)
        self.is_active = False
        self.tandemmodel = get_app().window.tandemmodel

        # signals and slots
        app = get_app()
        #app.signals.viewChanged.connect(self.action_set_view)

        window = app.window
        #window.channelsmodel.values_changed.connect(self.action_update_settings)
        self.action_update_settings
