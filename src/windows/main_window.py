from PySide6.QtWidgets import QMainWindow

from classes.logger import log
from classes.app import get_app
from windows.ui import main_window_ui
from windows.views.viewport import OrbitCameraViewer3d
from windows.models.displaymodel import DisplayModel
from windows.models.dicom_model import DicomModel
from windows.views.import_view import ImportView

class MainWindow(QMainWindow):

    def __init__(self, *args):
        super().__init__(*args)

        app = get_app()
        self.initialized = False

        log.info("Starting main window initialization")

        # TODO load user settings

        self.ui = main_window_ui.Ui_MainWindow()
        self.ui.setupUi(self)

        # TODO set keyboard shortcuts
        # TODO set theme
        # TODO set window variables (name, title, position in monitor) 
        # TODO connect signals to events

        # view signals send the new page's index
        # TODO change the values to specific widgets?
        self.ui.btn_import_view.pressed.connect(lambda: app.signals.viewChanged.emit(0))
        self.ui.btn_cylinder_view.pressed.connect(lambda: app.signals.viewChanged.emit(1))
        self.ui.btn_channels_view.pressed.connect(lambda: app.signals.viewChanged.emit(2))
        self.ui.btn_tandem_view.pressed.connect(lambda: app.signals.viewChanged.emit(3))
        self.ui.btn_export_view.pressed.connect(lambda: app.signals.viewChanged.emit(4))

        app.signals.viewChanged.connect(self.ui.viewswidget.setCurrentIndex)

    def initModels(self):
        # TODO initialize models
        self.displaymodel = DisplayModel()
        self.dicommodel = DicomModel()

    def initViews(self):
        # initialize canvas
        self.canvas = OrbitCameraViewer3d()
        self.ui.display_view_widget.layout().addWidget(self.canvas)
        self.canvas.InitDriver()
        self.display = self.canvas._display

        self.display.display_triedron()
        self.display.FitAll()

        self.displaymodel.shapes_changed.connect(self.canvas.update_display)

        # TODO views
        self.ui.page_import.layout().addWidget(ImportView())

        # show this window with resizing to ensure canvas is displayed properly
        self.showWithCanvas()  # shows and then resizes the window to properly display canvas
        self.initialized = True

        log.info("main window initialization complete")

    def showWithCanvas(self):
        # for the canvas widget to properly fit, we need to shrink the window slightly and then 
        # set it to the size as before
        size = [self.size().width(), self.size().height()]
        self.resize(size[0] - 1, size[1] - 1)  
        self.show()
        self.resize(size[0], size[1])
        
        



