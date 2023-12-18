from pathlib import Path

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Core.TopoDS import TopoDS_Compound, TopoDS_Shape

from PySide6.QtWidgets import QWidget, QFileDialog

from classes.app import get_app
from classes.logger import log
from classes.mesh.fileio import write_3d_file
import classes.pdf.template_reference as template_reference
from windows.models.shape_model import ShapeTypes, ShapeModel
from windows.ui.export_view_ui import Ui_Export_View
from windows.views.custom_view import display_action, CustomView

EXPORT_LABEL = "export"
BASEMAP = "basemap.png"
DEFAULT_NEEDLE_LENGTH = 160.0

materials = {
    ShapeTypes.CYLINDER: {"rgb": [0.2, 0.55, 0.55], "transparent": True},
    ShapeTypes.CHANNEL: {"rgb": [0.2, 0.55, 0.55], "transparent": True},
    ShapeTypes.TANDEM: {"rgb": [0.2, 0.55, 0.55], "transparent": False},
    ShapeTypes.SELECTED: {"rgb": [0.2, 0.55, 0.55], "transparent": True},
    ShapeTypes.EXPORT: {"rgb": [0.2, 0.55, 0.55], "transparent": True}
}


class Export_View(CustomView):

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

    def action_export_template_reference(self):
        filename = QFileDialog.getSaveFileName(
            self, 'Save solid as PDF', '', "PDF files (*.pdf)")
        
        # error checking
        if not filename:  # no file selected?
            log.info("no valid filename selected for importing")
            return
        
        window = get_app().window
        needle_length = self.ui.sb_needle_length.value()

        # generate pdf
        template_reference.generate_pdf(
            dicom=window.dicommodel.data,
            cylinder=window.cylindermodel.cylinder,
            channels=window.channelsmodel.get_visible_channels(),
            filepath=Path(filename[0]),
            needle_length=needle_length)

    def action_show_tandem(self, tandem_visible: bool):
        self.update_display()

    def on_close(self):
        log.debug(f"on close")

    # don't use @display_action because we want a unique view
    def on_open(self):
        log.debug(f"on open")

        # if tandem exists
        if self.window.tandemmodel.shape():
            self.ui.cb_tandem_shown.setEnabled(True)
        else:
            self.ui.cb_tandem_shown.setDisabled(True)

        self.shape = self._final_mesh()

        self.update_display()

    def update_display(self, *args):
        # export shape
        export_shape = ShapeModel(
            label=EXPORT_LABEL,
            shape=self.shape,
            shape_type=ShapeTypes.EXPORT
        )
        export_shape.material=materials[ShapeTypes.EXPORT]
        shapes = [export_shape]

        # tandem shape
        if self.ui.cb_tandem_shown.isChecked():
            tandemmodel = self.window.tandemmodel
            tandem = tandemmodel.shape()
            if tandem:
                tandem_shape = ShapeModel(
                    label=tandemmodel.get_label(),
                    shape=tandem,
                    shape_type=ShapeTypes.TANDEM
                ) 
                tandem_shape.material = materials[ShapeTypes.TANDEM]
                shapes.append(tandem_shape)
        
        self.window.displaymodel.show_shapes(shapes)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Export_View()
        self.ui.setupUi(self)
        self.window = get_app().window
        self.shape = None  # the model to export

        # signals and slots
        self.ui.btn_export_mesh.pressed.connect(self.action_export_mesh)
        self.ui.btn_export_shapes.pressed.connect(self.action_export_shapes)

        self.ui.sb_needle_length.setValue(DEFAULT_NEEDLE_LENGTH)
        self.ui.btn_export_template_reference.pressed.connect(self.action_export_template_reference)
        
        self.ui.cb_tandem_shown.stateChanged.connect(self.action_show_tandem)

    def _final_mesh(self) -> TopoDS_Shape:
        shape = self.window.cylindermodel.cylinder.shape()

        tandem_shape = self.window.tandemmodel.shape()
        if tandem_shape: shape = BRepAlgoAPI_Cut(shape, tandem_shape).Shape()

        for channel in self.window.channelsmodel.get_visible_channels():
            shape = BRepAlgoAPI_Cut(shape, channel.shape()).Shape()
        
        return shape

    def _final_shape(self) -> TopoDS_Compound:
        compound = TopoDS_Compound()  # houses all the shapes
        shape_tool = BRep_Builder()  # add shapes to the compound
        shape_tool.MakeCompound(compound)

        shape_tool.Add(compound, self.window.cylindermodel.cylinder.shape())

        tandem_shape = self.window.tandemmodel.shape()
        if tandem_shape: shape_tool.Add(compound, self.window.tandemmodel.shape())

        # place all channels in a sub compound
        channels_compound = TopoDS_Compound()
        channel_tool = BRep_Builder()
        channel_tool.MakeCompound(channels_compound)
        for channel in self.window.channelsmodel.get_visible_channels():
            channel_tool.Add(channels_compound, channel.shape())

        shape_tool.Add(compound, channels_compound)
        return compound