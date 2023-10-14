from PyQt5.QtWidgets import QFileDialog

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Extend.DataExchange import read_step_file, read_stl_file

import Application.Imports.import_dicom as dicom
from Application.Imports import *
from Presentation.MainWindow.core import MainWindow
import Presentation.Features.Cylinder.CylinderFunctions as cylFunctions
import Presentation.Features.NeedleChannels.NeedleFunctions as needleFunctions

import os


# https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html?highlight=qstringlist
def get_dicom_rs_file(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Open Patient RS File', '', "DICOM files (*.dcm)")[0]
    if len(filename) == 0:
        return
    
    cylFunctions.add_rs_file(window, filename)


def get_dicom_rp_file(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Open Patient RP File', '', "DICOM files (*.dcm)")[0]
    if len(filename) == 0:
        return

    needleFunctions.add_rp_file(window, filename)


def process_file(window: MainWindow, filepath: str):
    """receive a file and process it appropriately"""
    file_type = os.path.splitext(filepath)[1].lower()
        
    # if is DICOM?
    if file_type == ".dcm":
        if dicom.is_rs_file(filepath):
            cylFunctions.add_rs_file(window, filepath)
            return True
        if dicom.is_rp_file(filepath):
            needleFunctions.add_rp_file(window, filepath)
            return True
    else:
        print("Invalid file!")
        return False


def get_file_shape(filepath: str) -> TopoDS_Shape:
    # make sure the path exists otherwise OCE get confused
    if not os.path.exists(filepath):
        raise AssertionError(f"file does not exist: {filepath}")

    filepath = filepath.lower()
    file_dir, file_type = os.path.splitext(filepath)
    shape = None
    if file_type == ".stl":
        return read_stl_file(filepath)
    elif file_type == ".step" or file_type == ".stp":
        return read_step_file(filepath)
    else:
        print(f"Invalid tandem file! {filepath}")

    return None


