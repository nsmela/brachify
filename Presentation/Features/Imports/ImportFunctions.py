from PyQt5.QtWidgets import QFileDialog

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Extend.DataExchange import read_step_file, read_stl_file

import Application.Imports.import_dicom as dicom
from Application.Imports import import_dicom_planning

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


def get_dicom_folder(window: MainWindow) -> None:
    foldername = QFileDialog.getExistingDirectoryUrl(window, "Open patient folder").toLocalFile()
    if not foldername:  # no folder selected?
        return

    add_dicom_folder(window, foldername)


def add_dicom_folder(window: MainWindow, folder_path: str) -> None:
    files = [os.path.join(folder_path, file) for file in os.scandir(folder_path) if os.path.isfile(file)]

    print(f"{files}")

    # look for planning file first
    rp_file = None
    for file in files:
        if dicom.is_rp_file(file):
            rp_file = file
            break

    if not rp_file:  # if none of the files within the folder are a rp file
        print(f"No rs files where found at {folder_path}")

    # looking for the structure file
    rs_file = None
    for file in files:
        if dicom.is_rs_file(file):
            rs_file = file
            break

    if not rs_file:
        print(f"No rs file was found in {folder_path}")

    # get data from files
    print(f"Planning file is: {rp_file}")
    print(f"Structure file is: {rs_file}")
    data = dicom.load_dicom_data(rp_file, rs_file)
    cylinder = dicom.load_cylinder(data)
    cylFunctions.set_cylinder(window, cylinder)
    channels = dicom.load_channels(data)
    needleFunctions.set_channels(window, channels)


def process_file(window: MainWindow, filepath: str):
    """receive a dragged file or folder and process it appropriately"""
    if not os.path.isfile(filepath):  # not a file, could it be a folder?
        if os.path.isdir(filepath):
            add_dicom_folder(window, filepath)
        return

    # if the imported object is a file
    file_type = os.path.splitext(filepath)[1].lower()

    # if is DICOM?
    if file_type == ".dcm":
        if dicom.is_rs_file(filepath):
            cylFunctions.add_rs_file(window, filepath)
            import_dicom_planning.read_rs_file(filepath)
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
