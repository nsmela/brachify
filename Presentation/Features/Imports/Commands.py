from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMainWindow

from Presentation.MainWindow.core import MainWindow
from Presentation.MainWindow.ui_functions import UIFunctions

from Application.Imports.import_dicom import *

import os

class ImportFunctions(MainWindow):
    # https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html?highlight=qstringlist
    def get_dicom_rs_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Open Patient RS File', '', "DICOM files (*.dcm)")[0]
        UIFunctions.add_rs_file(self, filename)

    def get_dicom_rp_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Open Patient RP File', '', "DICOM files (*.dcm)")[0]
        UIFunctions.add_rp_file(self, filename)

    def get_tandem_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Select Tandem Model', '', "Supported files (*.stl *.3mf *.obj *.stp *.step)")[0]
        UIFunctions.add_tandem_file(self, filename)

    def process_file(self, filepath: str):
        '''receive a file and process it appropriately'''
        file_type = os.path.splitext(filepath)[1].lower()
        
        # if is DICOM?
        if file_type == ".dcm":
            if is_rs_file(filepath):
                UIFunctions.add_rs_file(self, filepath)
                return True
            if is_rp_file(filepath):
                UIFunctions.add_rp_file(self, filepath)
                return True
        
        supported_file_types = [".stl", ".3mf", ".obj", ".stp", ".step"]
        if file_type in supported_file_types:
            UIFunctions.add_tandem_file(self, filepath)
            return True
        else:
            print("Invalid file!")
            return False
        

