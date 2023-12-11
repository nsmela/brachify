from PySide6.QtWidgets import QWidget, QFileDialog

from classes.app import get_app
from classes.logger import log
from classes.dicom.fileio import read_dicom_folder
from classes.dicom.data import DicomData
from windows.ui.import_view_ui import Ui_Import_View
from windows.models.cylinder_model import CylinderModel
from windows.models.shape_model import ShapeTypes

colours = {
    ShapeTypes.CYLINDER: [1.0, 1.0, 0.2],
    ShapeTypes.CHANNEL: [0.5, 0.5, 0.5],
    ShapeTypes.TANDEM: [0.5, 0.5, 0.5],
    ShapeTypes.SELECTED: [0.5, 0.5, 0.2]}


class ImportView(QWidget):

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

    def action_update_import_label(self, data:DicomData):
        self.ui.label_file_info.setText(data.toString())

    def action_set_view(self, view_index: int):
        if view_index != 0: return  # this view is page 0, exit if not this view

        log.debug(f"setting display view")
        self.on_view_open()

    def on_view_open(self):
        displaymodel = get_app().window.displaymodel
        displaymodel.set_shape_colour(colours)
        displaymodel.set_transparent(False, True)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Import_View()
        self.ui.setupUi(self)

        # signals and slots
        self.ui.btn_import_folder.pressed.connect(self.action_import_dicom_folder)
        
        app = get_app()
        app.signals.viewChanged.connect(self.action_set_view)
        window = app.window
        window.dicommodel.values_changed.connect(self.action_update_import_label)

