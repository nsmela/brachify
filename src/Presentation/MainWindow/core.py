from PySide6 import QtCore
from PySide6.QtWidgets import QMainWindow

from Presentation.MainWindow.ui_main_ui import Ui_MainWindow

#from OCC.Display.backend import load_backend

#load_backend("pyside6")
#import OCC.Display.qtDisplay as qtDisplay
from Presentation.MainWindow.CustomViewer import OrbitCameraViewer3d
from .palettes import Palettes

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

import os


class MainWindow(QMainWindow):
    """Populates the UI file's functions to avoid needing to re-write a file each time the ui file is saved"""

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.isInit = False  # used to prevent others from referencing it before init
        self.ui.setupUi(self)
        Palettes.light(self)

        ########################################################################
        self.button_style = self.ui.btn_views_imports.styleSheet()

        ## PAGES
        ########################################################################
        from Presentation.MainWindow.ui_functions import UIFunctions
        # PAGE 1
        self.ui.btn_views_imports.clicked.connect(lambda: UIFunctions.setPage(self, UIFunctions.IMPORTS_VIEW))

        # PAGE 2
        self.ui.btn_views_cylinder.clicked.connect(lambda: UIFunctions.setPage(self, UIFunctions.CYLINDER_VIEW))

        # PAGE 3
        self.ui.btn_views_channels.clicked.connect(lambda: UIFunctions.setPage(self, UIFunctions.NEEDLE_CHANNELS_VIEW))

        # PAGE 4
        self.ui.btn_views_tandem.clicked.connect(lambda: UIFunctions.setPage(self, UIFunctions.TANDEM_VIEW))

        # PAGE 5
        self.ui.btn_views_exports.clicked.connect(lambda: UIFunctions.setPage(self, UIFunctions.EXPORTS_VIEW))

        UIFunctions.setPage(self, UIFunctions.IMPORTS_VIEW)

        ## pythonOCC Display
        ########################################################################
        self.canvas = OrbitCameraViewer3d(self) #qtDisplay.qtViewer3d(self)
        self.ui.model_frame.layout().addWidget(self.canvas)
        self.canvas.InitDriver()
        self.display = self.canvas._display

        a_box = BRepPrimAPI_MakeBox(10.0, 20.0, 30.0).Shape()
        self.ais_box = self.display.DisplayShape(a_box)[0]
        self.display.display_triedron()
        self.display.FitAll()

        self.isLocked = False  # used to prevent recalculating during variable assignments

        ## Imports Functions
        ########################################################################
        import Presentation.Features.Imports.ImportDisplay as importDisplay

        importDisplay.init(self)

        # drag and drop      
        self.ui.centralwidget.installEventFilter(self)

        ## Cylinder Stuff
        ########################################################################
        import Presentation.Features.Cylinder.CylinderDisplay as cylinderDisplay
        self.brachyCylinder = None
        cylinderDisplay.init(self)

        ## Needle Channel Stuff
        ########################################################################
        import Presentation.Features.NeedleChannels.NeedlesDisplay as needleDisplay
        self.needles = None
        self.isCylinderHidden = False
        needleDisplay.init(self)

        ## Tandem
        ########################################################################
        import Presentation.Features.Tandem.TandemDisplay as tandem
        self.tandem = None
        self.tandems = {}
        self.tandem_index = -1
        tandem.init(self)

        ## Exports
        ########################################################################
        import Presentation.Features.Exports.ExportFunctions as exports
        self.ui.btn_export_stl.clicked.connect(lambda: exports.export_stl(self))
        self.ui.btn_export_pdf.clicked.connect(lambda: exports.export_pdf(self))
        ## Display variables
        ########################################################################
        self.display_cylinder = None
        self.display_needles = None
        self.display_needles_list = []
        self.needles_active_index = -1
        self.display_tandem = None
        self.display_export = None

        ## Init Completed
        ########################################################################
        self.isInit = True

    # https://github.com/tpaviot/pythonocc-demos/issues/72#event-10551747046
    def showProperly(self):
        size = [self.size().width(), self.size().height()]
        self.resize(size[0] - 1, size[1] - 1)
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
