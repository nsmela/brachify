################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################
from turtle import Vec2D
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore

## ==> GUI FILE
from Presentation.MainWindow.core import MainWindow
from Presentation.Features.NeedleChannels.needlesModel import NeedlesModel

## Functions
from Application.Imports.import_dicom_structure import read_cylinder_file
from Application.Imports.import_dicom_planning import Rotate_Cloud, read_needles_file
from Application.BRep.channel import *

import numpy as np

from Presentation.MainWindow.display_functions import DisplayFunctions

class UIFunctions(MainWindow):

    def setPage(self, index: int):
        oldStyle = self.button_style
        stylesheet = "QPushButton{background-color: rgb(85, 170, 255);}"
        self.ui.btn_page_1.setStyleSheet(oldStyle)
        self.ui.btn_page_2.setStyleSheet(oldStyle)
        self.ui.btn_page_3.setStyleSheet(oldStyle)
        self.ui.btn_page_4.setStyleSheet(oldStyle)
        self.ui.btn_page_5.setStyleSheet(oldStyle)
        
        if index == 0:
            self.ui.btn_page_1.setStyleSheet(stylesheet)
        elif index == 1:
            self.ui.btn_page_2.setStyleSheet(stylesheet)
        elif index == 2:
            self.ui.btn_page_3.setStyleSheet(stylesheet)
        elif index == 3:
            self.ui.btn_page_4.setStyleSheet(stylesheet)
        elif index == 4:
            self.ui.btn_page_5.setStyleSheet(stylesheet)

        if index == 0:
            DisplayFunctions.navigate_to_imports(self)
        elif index == 1:
            DisplayFunctions.navigate_to_cylinder(self)
        elif index == 2:
            DisplayFunctions.navigate_to_channels(self)
        elif index == 3:
            DisplayFunctions.navigate_to_tandem(self)
        elif index == 4:
            DisplayFunctions.navigate_to_exports(self)
        
    def add_rs_file(self, filepath: str) -> None:
        self.ui.lineedit_dicom_rs.setText(filepath)
        self.brachyCylinder = read_cylinder_file(filepath=filepath)
        
        self.ui.cylinderLengthSpinBox.setValue(self.brachyCylinder.length)
        self.ui.cylinderRadiusSpinBox.setValue(self.brachyCylinder.radius)

        self.display_cylinder = self.brachyCylinder.shape
        
        UIFunctions.setPage(self, 1)

    def add_rp_file(self, filepath: str) -> None:
        self.ui.lineedit_dicom_rp.setText(filepath)
        
        # get data from dicom
        channels =  read_needles_file(filepath)
        
        # offset each point
        if self.brachyCylinder:
            V2 = np.array([0,0,1])
            cyl_vec = np.array(self.brachyCylinder.tip) - np.array(self.brachyCylinder.base)
            for i, c in enumerate(channels):
                newpoints = np.array(c.rawPoints) - self.brachyCylinder.base
                newpoints = Rotate_Cloud(newpoints, cyl_vec, V2)
                channels[i].points = list(list(points) for points in newpoints)
        self.needles = NeedlesModel(channels=channels)
        self.ui.channelsListView.setModel(self.needles)

        self.display_needles = []
        for channel in self.needles.channels:
            if self.display_needles:
                self.display_needles = BRepAlgoAPI_Fuse(self.display_needles, generate_stacked_fused(channel.points)).Shape()
            else:
                self.display_needles = generate_stacked_fused(channel.points)

        UIFunctions.setPage(self, 2)
        
    def add_tandem_file(self, filepath: str) -> None:
        self.ui.lineedit_tandem.setText(filepath)