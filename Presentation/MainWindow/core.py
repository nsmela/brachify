from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow


from Presentation.MainWindow.ui_main import Ui_MainWindow

from OCC.Display.backend import load_backend
load_backend("qt-pyqt5")
import OCC.Display.qtDisplay as qtDisplay

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

import os

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        from Presentation.MainWindow.ui_functions import UIFunctions
        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.ui.Btn_Toggle.clicked.connect(lambda: UIFunctions.toggleMenu(self, 250, True))
        self.button_style = self.ui.btn_page_1.styleSheet()
        
        ## PAGES
        ########################################################################
        from Presentation.MainWindow.ui_functions import UIFunctions
        # PAGE 1
        self.ui.btn_page_1.clicked.connect(lambda: UIFunctions.setPage(self, 0))

        # PAGE 2
        self.ui.btn_page_2.clicked.connect(lambda: UIFunctions.setPage(self, 1))

        # PAGE 3
        self.ui.btn_page_3.clicked.connect(lambda: UIFunctions.setPage(self, 2))
        
        # PAGE 4
        self.ui.btn_page_4.clicked.connect(lambda: UIFunctions.setPage(self, 3))
        
        # PAGE 5
        self.ui.btn_page_5.clicked.connect(lambda: UIFunctions.setPage(self, 4))
        
        UIFunctions.setPage(self, 0)
        
        ## pythonOCC Display
        ########################################################################
        self.canvas = qtDisplay.qtViewer3d(self)
        self.ui.model_frame.layout().addWidget(self.canvas)
        size = self.ui.model_frame.size()
        print(size)
        self.canvas.resize(640, 640)
        self.canvas.InitDriver()
        self.display = self.canvas._display
        
        a_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
        self.ais_box = self.display.DisplayShape(a_box)[0]
        self.display.FitAll()
        
        ## Imports Functions
        ########################################################################
        from Presentation.Features.Imports.Commands import  ImportFunctions

        self.ui.btn_import_dicom_rs.clicked.connect(lambda: ImportFunctions.get_dicom_rs_file(self))
        self.ui.btn_import_dicom_rp.clicked.connect(lambda: ImportFunctions.get_dicom_rp_file(self))
        self.ui.btn_import_tandem.clicked.connect(lambda: ImportFunctions.get_tandem_file(self))
        
        # drag and drop      
        self.ui.centralwidget.installEventFilter(self)
        
        
    def eventFilter(self, widget, event):
        from Presentation.Features.Imports.Commands import ImportFunctions
        
        if event.type() == QtCore.QEvent.Type.DragEnter:
            event.acceptProposedAction()
            return True
        if event.type() == QtCore.QEvent.Type.DragMove:
            event.acceptProposedAction()
            return True
        elif event.type() == QtCore.QEvent.Type.Drop:
            for url in event.mimeData().urls():
                filepath = url.url().replace("file:///", "")
                result = ImportFunctions.process_file(self, filepath)
            return True
        return False