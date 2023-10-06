################################################################################
##
## BY: WANDERSON M.PIMENTA
## PROJECT MADE WITH: Qt Designer and PySide2
## V: 1.0.0
##
################################################################################
from turtle import Vec2D
from typing import Self
from PyQt5 import QtCore

## ==> GUI FILE
from Presentation.MainWindow.core import MainWindow
from Presentation.MainWindow.display_functions import DisplayFunctions
import Presentation.Features.Imports.ImportDisplay as importDisplay 
import Presentation.Features.Cylinder.CylinderDisplay as cylDisplay 
import Presentation.Features.NeedleChannels.NeedlesDisplay as needleDisplay

## Functions

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
            importDisplay.view(self)
        elif index == 1:
            cylDisplay.view(self)
        elif index == 2:
            needleDisplay.view(self)
        elif index == 3:
            DisplayFunctions.navigate_to_tandem(self)
        elif index == 4:
            DisplayFunctions.navigate_to_exports(self)
        
