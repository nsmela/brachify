from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMainWindow

from OCC.Core.TopoDS import TopoDS_Shape

from Presentation.MainWindow.core import MainWindow


from Presentation.Features.NeedleChannels.needlesModel import NeedlesModel

import Application.Imports.import_dicom_structure as dicom_structure
import Application.Imports.import_dicom_planning as dicom_planning
import Application.Imports.import_dicom as dicom

from Core.Models.Tandem import TandemModel

import numpy as np

import os


# https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html?highlight=qstringlist
def get_dicom_rs_file(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Open Patient RS File', '', "DICOM files (*.dcm)")[0]
    if len(filename) == 0:
        return
    
    add_rs_file(window, filename)


def get_dicom_rp_file(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Open Patient RP File', '', "DICOM files (*.dcm)")[0]
    if len(filename) == 0:
        return
    
    add_rp_file(window, filename)


def get_tandem_file(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Select Tandem Model', '', "Supported files (*.stl *.3mf *.obj *.stp *.step)")[0]
    if len(filename) == 0:
        return
    
    add_tandem_file(window, filename)


def process_file(window: MainWindow, filepath: str):
    '''receive a file and process it appropriately'''
    file_type = os.path.splitext(filepath)[1].lower()
        
    # if is DICOM?
    if file_type == ".dcm":
        if dicom.is_rs_file(filepath):
            add_rs_file(window, filepath)
            return True
        if dicom.is_rp_file(filepath):
            add_rp_file(window, filepath)
            return True
        
    supported_file_types = [".stl", ".3mf", ".obj", ".stp", ".step"]
    if file_type in supported_file_types:
        add_tandem_file(window, filepath)
        return True
    else:
        print("Invalid file!")
        return False
        

def add_rs_file(window: MainWindow, filepath: str) -> None:
    window.ui.lineedit_dicom_rs.setText(filepath)
    window.brachyCylinder = dicom_structure.read_cylinder_file(filepath=filepath)
    
    window.isLocked = True
    window.ui.cylinderRadiusSpinBox.setValue(window.brachyCylinder.radius * 2)
    window.ui.cylinderLengthSpinBox.setValue(window.brachyCylinder.length)
    window.ui.checkbox_cylinder_base.setChecked(window.brachyCylinder.expand_base)

    window.display_cylinder = window.brachyCylinder.shape()
    window.isLocked = False
    
    from Presentation.MainWindow.ui_functions import UIFunctions
    UIFunctions.setPage(window, 1)


def add_rp_file(window: MainWindow, filepath: str) -> None:
    window.ui.lineedit_dicom_rp.setText(filepath)
        
    # get data from dicom
    channels =  dicom_planning.read_needles_file(filepath)
        
    # offset each point
    if window.brachyCylinder:
        V2 = np.array([0,0,1]) # z axis reference, the direction we want the cylinder and needles to go
        tip = np.array(window.brachyCylinder.tip)
        base = np.array(window.brachyCylinder.base)
        cyl_vec =  tip - base # the cylinder's original vector
        cyl_length = np.linalg.norm(cyl_vec)
        offset_vector = np.array([0,0, - cyl_length]) # normalized direction from tip to base
        for i, c in enumerate(channels):
            newpoints = np.array(c.rawPoints) - base
            newpoints = dicom_planning.Rotate_Cloud(newpoints, cyl_vec, V2)
            newpoints = newpoints - offset_vector
            channels[i].points = list(list(points) for points in newpoints)
    window.needles = NeedlesModel(channels=channels)
    for needle in window.needles.channels:
        window.ui.channelsListWidget.addItem(needle.channelId)

    diameter = 3.00
        
    window.ui.channelDiameterSpinBox.setValue(diameter)
    from Presentation.MainWindow.ui_functions import UIFunctions
    UIFunctions.setPage(window, 2)


def add_tandem_file(window: MainWindow, filepath: str) -> None:

    # make sure the path exists otherwise OCE get confused
    if not os.path.exists(filepath):
        raise AssertionError(f"file does not exist: {filepath}")

    filepath = filepath.lower()
    file_dir, file_type = os.path.splitext(filepath)
    shape = None
    if file_type == ".stl":
        shape = import_stl(filepath)
    elif file_type == ".step" or file_type == ".stp":
        shape = import_step(filepath)
    else:
        print(f"Invalid tandem file! {filepath}")
        return
    
    # global Tandem class
    window.tandem = Tandem()
    window.tandem.shape = shape
    
    window.ui.lineedit_tandem.setText(filepath)
    
    from Presentation.MainWindow.ui_functions import UIFunctions
    UIFunctions.setPage(window, 3)

def import_stl(filepath:str) -> TopoDS_Shape:
    from OCC.Extend.DataExchange import read_stl_file
    
    return read_stl_file(filepath)

def import_step(filepath:str) -> TopoDS_Shape:
    from OCC.Extend.DataExchange import read_step_file
    return read_step_file(filepath)