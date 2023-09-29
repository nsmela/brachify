from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMainWindow

from Presentation.MainWindow.core import MainWindow
from Presentation.MainWindow.ui_functions import UIFunctions


class ImportFunctions(MainWindow):
    # https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html?highlight=qstringlist
    def get_dicom_rs_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Open Patient RS File', '', "DICOM files (*.dcm)")
        UIFunctions.add_rs_file(self, filename[0])

    def get_dicom_rp_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Open Patient RP File', '', "DICOM files (*.dcm)")
        UIFunctions.add_rp_file(self, filename[0])

    def get_tandem_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Select Tandem Model', '', "Supported files (*.stl *.3mf *.obj *.stp *.step)")
        UIFunctions.add_tandem_file(self, filename[0])    
