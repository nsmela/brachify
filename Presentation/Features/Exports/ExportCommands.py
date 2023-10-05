from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMainWindow

from OCC.Extend.DataExchange import write_stl_file
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone

from Presentation.MainWindow.core import MainWindow

import os


def export_stl(window:MainWindow) -> None:
    # ref: https://github.com/tpaviot/pythonocc-demos/blob/master/examples/core_export_stl.py
    filename = QFileDialog.getSaveFileName(window, 'Save solid as STL', '', "STL files (*.stl)")[0]

    # set the directory where to output the
    stl_output_dir = os.path.abspath(os.path.dirname(filename))
    filename =  os.path.basename(filename)
    # make sure the path exists otherwise OCE get confused
    if not os.path.isdir(stl_output_dir):
        raise AssertionError(f"wrong path provided: {stl_output_dir}")

    # then we change the mesh resolution, and export as binary
    stl_high_resolution_file = os.path.join(stl_output_dir, filename)
    # we set the format to binary
    write_stl_file(
        window.display_export,
        stl_high_resolution_file,
        mode="binary",
        linear_deflection=0.5,
        angular_deflection=0.3,
    )