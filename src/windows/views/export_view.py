from OCC.Core.BRep import BRep_Builder

from PySide6.QtWidgets import QWidget, QFileDialog

from classes.app import get_app
from classes.logger import log
from classes.mesh.fileio import write_3d_file
from windows.models.shapemodel import ShapeModel
from windows.ui.export_view_ui import Ui_Export_View


class Export_View(QWidget):

    def actionExportMesh(self):
        from OCC.Core.TopoDS import TopoDS_Compound
        filename = QFileDialog.getSaveFileName(
            self, "Save model", "", "BRep file (*.step *.stp);; STL File (*.stl);; All files (*.*))", "")

        if not filename:  # no file selected?
            log.info("no valid filename selected for importing")
            return

        log.info(f"file {filename} has been selected for exporting")

        compound = TopoDS_Compound()
        shape_tool = BRep_Builder()
        shape_tool.MakeCompound(compound)
        app = get_app()
        shapes = {sm: sm.shape for sm in app.window.displaymodel.shapes.values()}
        for shape in shapes.values():
            shape_tool.Add(compound, shape)

        write_3d_file(filename[0], compound)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Export_View()
        self.ui.setupUi(self)

        # signals and slots
        self.ui.btn_export_models.pressed.connect(self.actionExportMesh)
