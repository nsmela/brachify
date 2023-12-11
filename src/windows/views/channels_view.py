from PySide6.QtWidgets import QWidget, QListWidgetItem

from classes.app import get_app
from classes.logger import log
from classes.dicom.data import DicomData
from windows.ui.channels_view_ui import Ui_Channels_View
from windows.models.channels_model import ChannelsModel
from windows.models.cylinder_model import CylinderModel
from windows.models.shape_model import ShapeTypes

colours = {
    ShapeTypes.CYLINDER: [1.0, 1.0, 1.0],
    ShapeTypes.CHANNEL: [0.2, 0.55, 0.55],
    ShapeTypes.TANDEM: [1.0, 1.0, 1.0],
    ShapeTypes.SELECTED: [0.5, 0.5, 0.2]}


class ChannelsView(QWidget):

    def action_select_channel(self, item: QListWidgetItem):
        log.debug(f"action: select channel")
        if type(item) is type(None): return None
        else: label = item.text()

        log.debug(f"selecting {label} channel")
        try:
            model = get_app().window.channelsmodel
            model.set_selected_channels(label)
        except Exception as error_message:
            log.critical(f"failed selecting channel from list view: \n{error_message}")

    def action_set_diameter(self):
        log.debug(f"action: set channel diameter")
        diameter = self.ui.spinbox_diameter.value()
        log.debug(f"setting channel diameters to: {diameter}")
        get_app().window.channelsmodel.set_diameter(diameter)

    def action_set_tandem(self):
        log.debug(f"setting channel's tandem status")

        model = get_app().window.channelsmodel
        channel_label = model.get_selected_channel()

        # set or clear the tandem channel
        label = None
        if channel_label != model.tandem_channel: label = channel_label
        model.set_tandem(label)

    def action_set_view(self, view_index: int):
        log.debug(f"action: set channel view")
        if view_index != 2:
            self.on_view_close()
            return  # this view is page 1, exit if not this view

        if not self.is_active:
            log.debug(f"switching to channels view")
            self.on_view_open()

    def action_toggle_channel_disable(self):
        log.debug(f"toggling channel's disabled status")
        model = get_app().window.channelsmodel
        channel_label = model.get_selected_channel()   
        model.toggle_channel_enabled(channel_label)

    def action_update_settings(self):
        if not self.is_active: return  # this view isn't displayed

        log.debug(f"updating channels view")
        
        # diameter spin box
        model = get_app().window.channelsmodel
        self.ui.spinbox_diameter.setValue(model.diameter)

        # channels list
        selected_channel = model.get_selected_channel()
        self.ui.listwidget_channels.blockSignals(True)  # prevents accidently emitting signals
        self.ui.listwidget_channels.clear()          
        for row, channel in enumerate(model.channels.values()):
            new_item = QListWidgetItem()
            new_item.setText(channel.label)
            self.ui.listwidget_channels.addItem(new_item)
            if selected_channel is not None and \
               selected_channel == channel.label:
                self.ui.listwidget_channels.setCurrentRow(row)
        self.ui.listwidget_channels.blockSignals(False)

        # selected channel
        # enable/disable buttons if any channel is selected
        any_selected = selected_channel != None
        self.ui.btn_enable.setEnabled(any_selected)
        self.ui.btn_set_tandem.setEnabled(any_selected)
        
        label = model.get_selected_channel()
        is_disabled = model.is_channel_disabled(label)
        is_tandem = model.is_channel_tandem(label)

        if is_disabled: self.ui.btn_enable.setText("Enable")
        else: self.ui.btn_enable.setText("Disable")

        if is_tandem: self.ui.btn_set_tandem.setText("Clear Tandem")
        else: self.ui.btn_set_tandem.setText("Set as Tandem")
        
    def on_view_open(self):
        log.debug(f"on view open")
        self.is_active = True

        canvas = get_app().window.canvas
        channelsmodel = get_app().window.channelsmodel
        canvas.sig_topods_selected.connect(channelsmodel.set_selected_shapes)

        displaymodel = get_app().window.displaymodel
        displaymodel.set_shape_colour(colours)
        displaymodel.set_transparent(True)
        channelsmodel.update()

        self.action_update_settings()

    def on_view_close(self):
        if not self.is_active: return
        log.debug(f"on view close")

        self.is_active = False
        try:
            displaymodel = get_app().window.displaymodel
            displaymodel.set_transparent(False)
            
            canvas = get_app().window.canvas
            channelsmodel = get_app().window.channelsmodel
            canvas.sig_topods_selected.disconnect(channelsmodel.set_selected_shapes)
        except RuntimeError as error_message:  # incase the signal isn't connected
            log.warning(f"{error_message}")

    def __init__(self):
        super().__init__()
        self.ui = Ui_Channels_View()  # the converted python file from the ui file
        self.ui.setupUi(self)
        self.is_active = False

        # signals and slots
        self.ui.btn_apply_diameter.pressed.connect(self.action_set_diameter)
        self.ui.listwidget_channels.currentItemChanged.connect(self.action_select_channel)
        self.ui.btn_enable.pressed.connect(self.action_toggle_channel_disable)
        self.ui.btn_set_tandem.pressed.connect(self.action_set_tandem)

        app = get_app()
        app.signals.viewChanged.connect(self.action_set_view)

        window = app.window
        window.channelsmodel.values_changed.connect(self.action_update_settings)

        self.action_update_settings()
