from PyQt5 import QtCore
from PyQt5.QtWidgets import QAbstractItemView, QMainWindow

from Presentation.MainWindow.ui_main import Ui_MainWindow

from OCC.Display.backend import load_backend

load_backend("qt-pyqt5")
import OCC.Display.qtDisplay as qtDisplay

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

import os


class MainWindow(QMainWindow):
    """Populates the UI file's functions to avoid needing to re-write a file each time the ui file is saved"""

    def __init__(self):
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.isInit = False  # used to prevent others from referencing it before init
        self.ui.setupUi(self)

        from Presentation.MainWindow.ui_functions import UIFunctions
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
        self.canvas = qtDisplay.qtViewer3d(self)
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
        import Presentation.Features.Imports.ImportFunctions as imports

        self.ui.btn_import_dicom_rs.clicked.connect(lambda: imports.get_dicom_rs_file(self))
        self.ui.btn_import_dicom_rp.clicked.connect(lambda: imports.get_dicom_rp_file(self))

        # drag and drop      
        self.ui.centralwidget.installEventFilter(self)

        ## Cylinder Stuff
        ########################################################################
        import Presentation.Features.Cylinder.CylinderFunctions as cylinder
        self.brachyCylinder = None
        self.cylinder_offset_direction = [0.0, 0.0, 0.0]
        self.cylinder_offset_length = 0.0

        self.ui.cylinderRadiusSpinBox.valueChanged.connect(lambda: cylinder.setRadius(self))
        self.ui.cylinderLengthSpinBox.valueChanged.connect(lambda: cylinder.setLength(self))
        self.ui.checkbox_cylinder_base.toggled.connect(lambda: cylinder.setBase(self))

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
        self.tandem_offset_position = [0.0, 0.0, 0.0]  # set by needle channels and offset by cylinder origin
        self.tandem_offset_rotation = 0.0  # set by the tandem channel in needle channels
        tandem.init(self)

        ## Exports
        ########################################################################
        import Presentation.Features.Exports.ExportFunctions as exports
        self.ui.btn_export_stl.clicked.connect(lambda: exports.export_stl(self))

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
