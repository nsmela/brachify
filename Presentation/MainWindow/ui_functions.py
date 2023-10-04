################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################
from turtle import Vec2D
from typing import Self
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from PyQt5.QtCore import QPropertyAnimation
from PyQt5 import QtCore
from Presentation.Features.needle_functions import NeedleFunctions

## ==> GUI FILE
from Presentation.MainWindow.core import MainWindow
from Presentation.Features.NeedleChannels.needlesModel import NeedlesModel
from Presentation.MainWindow.display_functions import DisplayFunctions

## Functions
from Application.Imports.import_dicom_structure import read_cylinder_file
from Application.Imports.import_dicom_planning import Rotate_Cloud, read_needles_file
from Application.BRep.channel import *
from OCC.Extend.DataExchange import read_step_file

import numpy as np
import os


class UIFunctions(MainWindow):

    def setPage(self, index: int):
        oldStyle = self.button_style
        stylesheet = "QPushButton{background-color: rgb(85, 170, 255);}"
        buttons = [
            self.ui.btn_views_imports,
            self.ui.btn_views_cylinder,
            self.ui.btn_views_channels,
            self.ui.btn_views_tandem,
            self.ui.btn_views_exports]
        
        for button in buttons:
            button.setStyleSheet(oldStyle)
        
        buttons[index].setStyleSheet(stylesheet)

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
        
        self.ui.cylinderRadiusSpinBox.setValue(self.brachyCylinder.radius * 2)
        self.ui.cylinderLengthSpinBox.setValue(self.brachyCylinder.length)
        self.ui.checkbox_cylinder_base.setChecked(self.brachyCylinder.expand_base)

        self.display_cylinder = self.brachyCylinder.shape()
        
        # cylinder view ui values
        
        UIFunctions.setPage(self, 1)


    def add_rp_file(self, filepath: str) -> None:
        self.ui.lineedit_dicom_rp.setText(filepath)
        
        # get data from dicom
        channels =  read_needles_file(filepath)
        
        # offset each point
        if self.brachyCylinder:
            V2 = np.array([0,0,1]) # z axis reference, the direction we want the cylinder and needles to go
            tip = np.array(self.brachyCylinder.tip)
            base = np.array(self.brachyCylinder.base)
            cyl_vec =  tip - base # the cylinder's original vector
            cyl_length = np.linalg.norm(cyl_vec)
            offset_vector = np.array([0,0, - cyl_length]) # normalized direction from tip to base
            for i, c in enumerate(channels):
                newpoints = np.array(c.rawPoints) - base
                newpoints = Rotate_Cloud(newpoints, cyl_vec, V2)
                newpoints = newpoints - offset_vector
                channels[i].points = list(list(points) for points in newpoints)
        self.needles = NeedlesModel(channels=channels)
        for needle in self.needles.channels:
            self.ui.channelsListWidget.addItem(needle.channelId)

        diameter = 3.00
        #self.display_needles = []
        #for channel in self.needles.channels:
        #    if self.display_needles:
        #        self.display_needles = BRepAlgoAPI_Fuse(self.display_needles, generate_stacked_fused(channel.points, radius)).Shape()
        #    else:
        #        self.display_needles = generate_stacked_fused(channel.points, radius)
        
        self.ui.channelDiameterSpinBox.setValue(diameter)
        NeedleFunctions.__recalculate__(self)
        UIFunctions.setPage(self, 2)
        
    def add_tandem_file(self, filepath: str) -> None:
        self.ui.lineedit_tandem.setText(filepath)

        # make sure the path exists otherwise OCE get confused
        if not os.path.exists(filepath):
            raise AssertionError(f"file does not exist: {filepath}")

        self.display_tandem = read_step_file(filepath)
        
        UIFunctions.setPage(self, 3)