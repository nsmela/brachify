from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMainWindow

from Presentation.MainWindow.core import MainWindow
from Presentation.MainWindow.ui_functions import UIFunctions

from Application.Imports.import_dicom import *

import os

class ImportFunctions(MainWindow):
    # https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html?highlight=qstringlist
    def get_dicom_rs_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Open Patient RS File', '', "DICOM files (*.dcm)")
        file_type = os.path.splitext(filename[0])

        UIFunctions.add_rs_file(self, filename[0])

    def get_dicom_rp_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Open Patient RP File', '', "DICOM files (*.dcm)")
        UIFunctions.add_rp_file(self, filename[0])

    def get_tandem_file(self) -> None:
        filename = QFileDialog.getOpenFileName(self, 'Select Tandem Model', '', "Supported files (*.stl *.3mf *.obj *.stp *.step)")
        UIFunctions.add_tandem_file(self, filename[0])

    def process_file(self, filepath: str):
        file_type = os.path.splitext(filepath)[1]
        
        # if is DICOM?
        if file_type == ".dcm":
            if is_rs_file(filepath):
                print("RS file loaded!")
                return True
            if is_rp_file(filepath):
                print("RP file loaded!")
                return True
        
        if file_type == ".stl":
            print("STL file loaded!")
        elif file_type == ".3mf":
            print("3MF file loaded!")
        elif file_type == ".obj":
            print("OBJ file loaded!")
        elif file_type == ".stp":
            print("STP file loaded!")
        elif file_type == ".step":
            print("STEP file loaded!")
        else:
            print("Invalid file!")
        

