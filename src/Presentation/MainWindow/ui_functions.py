##  GUI FILE
from Presentation.MainWindow.core import MainWindow
import Presentation.Features.Imports.ImportDisplay as importDisplay
import Presentation.Features.Cylinder.CylinderDisplay as cylDisplay 
import Presentation.Features.NeedleChannels.NeedlesDisplay as needleDisplay
import Presentation.Features.Tandem.TandemDisplay as tandemDisplay
import Presentation.Features.Exports.ExportDisplay as exportsDisplay

## Functions

import numpy as np
import os


class UIFunctions:
    IMPORTS_VIEW = "Imports View"
    CYLINDER_VIEW = "Cylinder View"
    NEEDLE_CHANNELS_VIEW = "Needle Channels View"
    EXPORTS_VIEW = "Exports View"
    TANDEM_VIEW = "Tandem View"


    def setPage(window: MainWindow, view_name: str):
        style_unclicked = window.button_style

        # TODO have this style set within the designer
        style_clicked = "QPushButton{background-color: rgb(85, 170, 255);}"

        views = {
            UIFunctions.IMPORTS_VIEW: {"Button": window.ui.btn_views_imports, "Index": 0, "Display": importDisplay.view},
            UIFunctions.CYLINDER_VIEW: {"Button": window.ui.btn_views_cylinder, "Index": 1, "Display": cylDisplay.view},
            UIFunctions.NEEDLE_CHANNELS_VIEW: {"Button": window.ui.btn_views_channels, "Index": 2, "Display": needleDisplay.view},
            UIFunctions.TANDEM_VIEW: {"Button": window.ui.btn_views_tandem, "Index": 3, "Display": tandemDisplay.view},
            UIFunctions.EXPORTS_VIEW: {"Button": window.ui.btn_views_exports, "Index": 4, "Display": exportsDisplay.view}
        }

        for button in views.values():
            button["Button"].setStyleSheet(style_unclicked)
        
        views[view_name]["Button"].setStyleSheet(style_clicked) # set the active button's style
        window.ui.stackedWidget.setCurrentIndex(views[view_name]["Index"]) # set the stackedWidget's page
        views[view_name]["Display"](window) 


        
