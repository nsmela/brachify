from PySide6.QtWidgets import QWidget, QFileDialog

from classes.app import get_app
from classes.logger import log
from classes.mesh.fileio import read_3d_file, write_3d_file
from windows.models.shapemodel import ShapeModel
from windows.ui.mesh_view_ui import Ui_Mesh_View


class Mesh_View(QWidget):

    def actionImportMesh(self):
        filename = QFileDialog.getOpenFileName(
            self, "Open model", "", "Model files (*.step *.stp *.stl);; All files (*.*))", "")[0]

        if not filename:  # no file selected?
            log.info("no valid filename selected for importing")
            return

        log.info(f"file {filename} has been selected")

        shape = read_3d_file(filename=filename)
        shape_model = ShapeModel("main", shape)
        
        app = get_app()
        app.window.displaymodel.add_shape(shape_model)

    def setupUi(self):
        pass

    def __init__(self):
        super().__init__()
        self.ui = Ui_Mesh_View()
        self.ui.setupUi(self)

        # signals and slots
        self.ui.btn_import_mesh.pressed.connect(self.actionImportMesh)


