from PySide6.QtWidgets import QWidget, QFileDialog

from classes.app import get_app
from classes.logger import log
from classes.dicom.fileio import read_dicom_folder
from classes.dicom.data import DicomData
from windows.models.shape_model import ShapeTypes
from windows.ui.import_view_ui import Ui_Import_View
from windows.views.custom_view import display_action, CustomView

colours = {
    ShapeTypes.CYLINDER: [0.2, 0.55, 0.55],
    ShapeTypes.CHANNEL: [0.2, 0.55, 0.55],
    ShapeTypes.TANDEM: [0.2, 0.55, 0.55],
    ShapeTypes.SELECTED: [0.5, 0.5, 0.2]}


class ImportView(CustomView):

    @display_action
    def action_import_dicom_folder(self):
        foldername = QFileDialog.getExistingDirectoryUrl(
            self, "Open patient folder").toLocalFile()
        
        if not foldername:  # no folder selected?
            log.info("no valid filename selected for importing")
            return

        log.info(f"file {foldername} has been selected")

        data = read_dicom_folder(foldername)

        # Add patient and plan info to window
        app = get_app()
        window = app.window

        window.dicommodel.update(data)
        window.displaymodel.set_transparent(True)

    def action_update_import_label(self, data:DicomData):
        self.ui.label_file_info.setText(data.toString())

    @display_action
    def on_open(self):
        log.debug(f"on view open")
        displaymodel = get_app().window.displaymodel
        displaymodel.set_shape_colour(colours)
        displaymodel.set_transparent(True)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Import_View()
        self.ui.setupUi(self)

        # signals and slots
        self.ui.btn_import_folder.pressed.connect(self.action_import_dicom_folder)
        
        window = get_app().window
        window.dicommodel.values_changed.connect(self.action_update_import_label)

