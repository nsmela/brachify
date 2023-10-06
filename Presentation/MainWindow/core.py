from email.mime import application
from PyQt5 import QtCore
from PyQt5.QtWidgets import QAbstractItemView, QMainWindow

from Presentation.MainWindow.ui_main import Ui_MainWindow
from Core.Models.Cylinder import BrachyCylinder

from OCC.Display.backend import load_backend
load_backend("qt-pyqt5")
import OCC.Display.qtDisplay as qtDisplay

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

import os


class MainWindow(QMainWindow):
    '''Populates the UI file's functions to avoid needing to re-write a file each time the ui file is saved'''
    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        from Presentation.MainWindow.ui_functions import UIFunctions
        from Presentation.Features.NeedleChannels.needlesModel import NeedlesModel
        ## TOGGLE/BURGUER MENU
        ########################################################################
        self.button_style = self.ui.btn_views_imports.styleSheet()
        
        ## PAGES
        ########################################################################
        from Presentation.MainWindow.ui_functions import UIFunctions
        # PAGE 1
        self.ui.btn_views_imports.clicked.connect(lambda: UIFunctions.setPage(self, 0))

        # PAGE 2
        self.ui.btn_views_cylinder.clicked.connect(lambda: UIFunctions.setPage(self, 1))

        # PAGE 3
        self.ui.btn_views_channels.clicked.connect(lambda: UIFunctions.setPage(self, 2))
        
        # PAGE 4
        self.ui.btn_views_tandem.clicked.connect(lambda: UIFunctions.setPage(self, 3))
        
        # PAGE 5
        self.ui.btn_views_exports.clicked.connect(lambda: UIFunctions.setPage(self, 4))
        
        UIFunctions.setPage(self, 0)
        
        ## pythonOCC Display
        ########################################################################
        self.canvas = qtDisplay.qtViewer3d(self)
        self.ui.model_frame.layout().addWidget(self.canvas)
        self.canvas.InitDriver()
        self.display = self.canvas._display
        
        a_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
        self.ais_box = self.display.DisplayShape(a_box)[0]
        self.display.display_triedron()
        self.display.FitAll()

        self.isLocked = False # used to prevent recalculating during variable assignments
        
        ## Imports Functions
        ########################################################################
        import Presentation.Features.Imports.ImportFunctions as imports

        self.ui.btn_import_dicom_rs.clicked.connect(lambda: imports.get_dicom_rs_file(self))
        self.ui.btn_import_dicom_rp.clicked.connect(lambda: imports.get_dicom_rp_file(self))
        self.ui.btn_import_tandem.clicked.connect(lambda: imports.get_tandem_file(self))
        
        # drag and drop      
        self.ui.centralwidget.installEventFilter(self)
        
        ## Cylinder Stuff
        ########################################################################
        import Presentation.Features.Cylinder.CylinderFunctions as cylinder
        self.brachyCylinder = None  
        
        self.ui.cylinderRadiusSpinBox.valueChanged.connect(lambda: cylinder.setRadius(self))
        self.ui.cylinderLengthSpinBox.valueChanged.connect(lambda: cylinder.setLength(self))
        self.ui.checkbox_cylinder_base.toggled.connect(lambda: cylinder.setBase(self))

        ## Needle Channel Stuff
        ########################################################################
        import Presentation.Features.NeedleChannels.NeedleFunctions as needles
        self.needles = None
        self.isCylinderHidden = False;
        self.ui.checkBox_hide_cylinder.stateChanged.connect(lambda: needles.setCylinderVisibility(self))
        self.ui.channelDiameterSpinBox.valueChanged.connect(lambda: needles.recalculate(self))
        self.ui.channelsListWidget.itemSelectionChanged.connect( 
            lambda: needles.setActiveNeedleChannel(self, self.ui.channelsListWidget.currentRow()))
        self.ui.groupBox_5.setEnabled(False)
        self.ui.slider_needle_extension.valueChanged.connect(lambda: needles.setChannelOffset(self, 
                                           self.ui.slider_needle_extension.value()))
        self.ui.btn_channel_disable.clicked.connect(lambda: needles.setNeedleDisabled(self))

        ## Tandem
        ########################################################################
        import Presentation.Features.Tandem.TandemFunctions as tandemFunctions
        self.tandem = None
        
        ## Exports
        ########################################################################
        import Presentation.Features.Exports.ExportCommands as exports
        self.ui.btn_export_stl.clicked.connect(lambda: exports.export_stl(self))
        
        ## Display variables
        ########################################################################
        self.display_cylinder = None
        self.display_needles = None
        self.display_needles_list = []
        self.needles_active_index = -1
        self.display_tandem = None
        self.display_export = None
        

    # https://github.com/tpaviot/pythonocc-demos/issues/72#event-10551747046
    def showProperly(self):
        size = [self.size().width(), self.size().height()]
        self.resize(size[0]-1, size[1]-1)
        self.show()
        self.resize(size[0], size[1])

    # for dragging events
    def eventFilter(self, widget, event):
        import Presentation.Features.Imports.ImportFunctions as imports
        
        if event.type() == QtCore.QEvent.Type.DragEnter:
            event.acceptProposedAction()
            return True
        if event.type() == QtCore.QEvent.Type.DragMove:
            event.acceptProposedAction()
            return True
        elif event.type() == QtCore.QEvent.Type.Drop:
            for url in event.mimeData().urls():
                filepath = url.url().replace("file:///", "")
                result = imports.process_file(self, filepath)
            return True
        return False