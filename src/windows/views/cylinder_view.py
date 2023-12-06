from PySide6.QtWidgets import QWidget

from classes.app import get_app
from classes.logger import log
from classes.dicom.data import DicomData
from windows.ui.cylinder_view_ui import Ui_Cylinder_View
from windows.models.cylinder_model import CylinderModel
from classes.mesh.cylinder import BrachyCylinder

COLOURS_CYLINDER = [0.2, 0.55, 0.55,]
COLOURS_CHANNELS = [0.5, 0.5, 0.4]
COLOURS_TANDEM = [0.5, 0.5, 0.4]


class CylinderView(QWidget):

    def action_apply_settings(self):
        log.debug(f"applying cylinder settings")

        model = get_app().window.cylindermodel
        cylinder = model.cylinder

        diameter = self.ui.spinbox_diameter.value()
        length = self.ui.spinbox_length.value()
        add_base = self.ui.cb_add_base.isChecked()

        if cylinder.length != length:
            cylinder.length = length

            # send the new offset signal
            offset = length - BrachyCylinder.default_length() 
            get_app().signals.height_changed.emit(offset)

        cylinder.diameter = diameter
        cylinder.enableBase(add_base)  # this will force the cylinder's shape to be recalculated

        model.update_cylinder(cylinder)

    def action_update_settings(self, cylinder: BrachyCylinder):     
        log.debug(f"updating cylinder view's settings")
        model = get_app().window.cylindermodel
        
        if model.cylinder is None: return

        diameter = model.cylinder.diameter
        length = model.cylinder.length
        add_base = model.cylinder.expand_base
        
        self.ui.spinbox_diameter.setValue(diameter)
        self.ui.spinbox_length.setValue(length)
        self.ui.cb_add_base.setChecked(add_base)

    def action_set_view(self, view_index: int):
        if view_index != 1: return  # this view is page 1, exit if not this view

        log.debug(f"switching to cylinder view")

        colours = {}
        colours[CylinderModel.get_label()] = COLOURS_CYLINDER
        # TODO Needles color
        # TODO Tandem Color
        get_app().window.displaymodel.set_shape_colour(colours)

    def __init__(self):
        super().__init__()
        self.ui = Ui_Cylinder_View()  # the converted python file from the ui file
        self.ui.setupUi(self)

        # signals and slots
        self.ui.btn_apply_settings.pressed.connect(self.action_apply_settings)

        app = get_app()
        app.signals.viewChanged.connect(self.action_set_view)
        window = app.window
        window.cylindermodel.values_changed.connect(self.action_update_settings)

        self.action_update_settings(window.cylindermodel.cylinder)
