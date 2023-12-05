from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QWidget, QFileDialog

from classes.app import get_app
from classes.logger import log
from classes.dicom.fileio import read_dicom_folder
from windows.ui.import_view_ui import Ui_Import_View


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

    def setupUi(self):
        pass

    def __init__(self):
        super().__init__()
        self.ui = Ui_Import_View()
        self.ui.setupUi(self)

        # signals and slots
        self.ui.btn_import_mesh.pressed.connect(self.action_import_dicom_folder)
