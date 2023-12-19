from PySide6.QtWidgets import QWidget, QListWidgetItem

from classes.app import get_app
from classes.logger import log
from windows.models.shape_model import ShapeTypes
from windows.ui.channels_view_ui import Ui_Channels_View
from windows.views.custom_view import display_action, CustomView

materials = {
    ShapeTypes.CYLINDER: {"rgb": [0.8, 0.8, 0.8], "transparent": True},
    ShapeTypes.CHANNEL: {"rgb": [0.2, 0.55, 0.55], "transparent": False},
    ShapeTypes.TANDEM: {"rgb": [0.8, 0.8, 0.8], "transparent": True},
    ShapeTypes.SELECTED: {"rgb": [0.2, 0.2, 0.7], "transparent": False}
}


class ChannelsView(CustomView):

    @display_action
    def action_select_channel(self, item: QListWidgetItem, *args):
        log.debug(f"action: select channel")
        log.debug(f"{args}")
        if type(item) is type(None): return None
        else: label = item.text()

        log.debug(f"selecting {label} channel")
        try:
            self.channelsmodel.set_selected_channels(label)
        except Exception as error_message:
            log.critical(f"failed selecting channel from list view: \n{error_message}")

    @display_action
    def action_set_diameter(self):
        log.debug(f"action: set channel diameter")
        diameter = self.ui.spinbox_diameter.value()
        log.debug(f"setting channel diameters to: {diameter}")
        self.channelsmodel.set_diameter(diameter)

    @display_action
    def action_set_selected_shapes(self, *args, **kwargs):
        self.channelsmodel.set_selected_shapes(*args)

    @display_action
    def action_set_tandem(self):
        log.debug(f"setting channel's tandem status")

        model = get_app().window.channelsmodel
        channel_label = model.get_selected_channel()

        # set or clear the tandem channel
        label = None
        if channel_label != model.tandem_channel: label = channel_label
        model.set_tandem(label)

    @display_action
    def action_toggle_channel_disable(self):
        log.debug(f"toggling channel's disabled status")
        model = get_app().window.channelsmodel
        channel_label = model.get_selected_channel()   
        model.toggle_channel_enabled(channel_label)

    def action_update_settings(self):
        log.debug(f"updating channels view")
        
        # diameter spin box
        self.ui.spinbox_diameter.setValue(self.channelsmodel.diameter)

        # channels list
        selected_channel = self.channelsmodel.get_selected_channel()
        self.ui.listwidget_channels.blockSignals(True)  # prevents accidently emitting signals
        self.ui.listwidget_channels.clear()          
        for row, channel in enumerate(self.channelsmodel.channels.values()):
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
        
        label = self.channelsmodel.get_selected_channel()
        is_disabled = self.channelsmodel.is_channel_disabled(label)
        is_tandem = self.channelsmodel.is_channel_tandem(label)

        if is_disabled: self.ui.btn_enable.setText("Enable")
        else: self.ui.btn_enable.setText("Disable")

        if is_tandem: self.ui.btn_set_tandem.setText("Clear Tandem")
        else: self.ui.btn_set_tandem.setText("Set as Tandem")

    def on_close(self):
        log.debug(f"on close")

        channelsmodel = get_app().window.channelsmodel
        channelsmodel.clear_selected_channels()

        try:         
            canvas = get_app().window.canvas
            canvas.sig_topods_selected.disconnect(self.action_set_selected_shapes)
        except RuntimeError as error_message:  # incase the signal isn't connected
            log.warning(f"{error_message}")

    @display_action
    def on_open(self):
        log.debug(f"on open")

        canvas = get_app().window.canvas
        canvas.sig_topods_selected.connect(self.action_set_selected_shapes)

        displaymodel = get_app().window.displaymodel
        displaymodel.set_materials(materials)
        self.channelsmodel.update()

        self.action_update_settings()

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

        self.channelsmodel = get_app().window.channelsmodel
        self.channelsmodel.values_changed.connect(self.action_update_settings)

        self.action_update_settings()
