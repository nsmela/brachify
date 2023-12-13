from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shape

from PySide6.QtWidgets import QWidget, QFileDialog

from classes.app import get_app
from classes.logger import log
from classes.mesh.fileio import write_3d_file
from windows.models.shape_model import ShapeTypes, ShapeModel
from windows.ui.export_view_ui import Ui_Export_View

EXPORT_LABEL = "export"

colours = {
    ShapeTypes.CYLINDER: [1.0, 1.0, 1.0],
    ShapeTypes.CHANNEL: [1.0, 1.0, 1.0],
    ShapeTypes.TANDEM: [0.2, 0.55, 0.55],
    ShapeTypes.SELECTED: [0.5, 0.5, 0.2],
    ShapeTypes.EXPORT: [0.8, 0, 0]}

class Export_View(QWidget):

    def action_export_mesh(self):
        """
        Create a single mesh from boolean subtracting the channels and tandem from the cylinder
        """
        filename = QFileDialog.getSaveFileName(
            self, "Save model", "", "STL File (*.stl);; BRep file (*.step *.stp);; All files (*.*))", "")

        if not filename:  # no file selected?
            log.info("no valid filename selected for importing")
            return

        log.info(f"file {filename} has been selected for exporting")
        write_3d_file(filename[0], self.shape)

    def action_export_shapes(self):
        """
        Collect the shapes and export them in a single file
        """
        filename = QFileDialog.getSaveFileName(
            self, "Save model", "", "BRep file (*.step *.stp);;", "")

        if not filename:  # no file selected?
            log.info("no valid filename selected for importing")
            return

        log.info(f"file {filename} has been selected for exporting")
        compound = self._final_shape()
        write_3d_file(filename[0], compound)

    def on_view_close(self):
        log.debug(f"on view close")

    def on_view_open(self):
        log.debug(f"on view open")

        displaymodel = self.window.displaymodel
        displaymodel.set_shape_colour(colours)
        self.shape = self._final_mesh()
        shape_model = ShapeModel(
            label=EXPORT_LABEL,
            shape=self.shape,
            shape_type=ShapeTypes.EXPORT)
        shape_model.transparent = True

        displaymodel.show_shape(shape_model)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Export_View()
        self.ui.setupUi(self)
        self.window = get_app().window
        self.shape = None  # the model to export

        # signals and slots
        self.ui.btn_export_mesh.pressed.connect(self.action_export_mesh)
        self.ui.btn_export_shapes.pressed.connect(self.action_export_shapes)
        
    def _final_mesh(self) -> TopoDS_Shape:
        shape = self.window.cylindermodel.cylinder.shape()
        shape = BRepAlgoAPI_Cut(shape, self.window.tandemmodel.shape()).Shape()

        for channel in self.window.channelsmodel.channels.values():
            shape = BRepAlgoAPI_Cut(shape, channel.shape()).Shape()
        
        return shape

    def _final_shape(self) -> TopoDS_Compound:
        compound = TopoDS_Compound()  # houses all the shapes
        shape_tool = BRep_Builder()  # add shapes to the compound
        shape_tool.MakeCompound(compound)

        # cylinder and tandem
        shape_tool.Add(compound, self.window.cylindermodel.cylinder.shape())
        shape_tool.Add(compound, self.window.tandemmodel.shape())

        # place all channels in a sub compound
        channels_compound = TopoDS_Compound()
        channel_tool = BRep_Builder()
        channel_tool.MakeCompound(channels_compound)
        for channel in self.window.channelsmodel.channels.values():
            channel_tool.Add(channels_compound, channel.shape())

        shape_tool.Add(compound, channels_compound)
        return compound