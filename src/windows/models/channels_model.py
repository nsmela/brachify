from PySide6.QtCore import QObject, Signal

from OCC.Core.TopoDS import TopoDS_Compound

from classes.app import get_app
from classes.dicom.data import DicomData
from classes.logger import log
from classes.mesh.channel import NeedleChannel
from windows.models.shape_model import ShapeModel, ShapeTypes

CHANNELS_LABEL = "applicator_"


class ChannelsModel(QObject):

    values_changed = Signal()

    def is_channel_disabled(self, label: str) -> bool:
        return label in self.disabled_channels
    
    def is_channel_tandem(self, label:str) -> bool:
        return label == self.tandem_channel

    def get_selected_channel(self) -> str:
        if not self.selected_channels: return None
        return self.selected_channels[0]

    # Slotted to Dicom Model's update
    def load_data(self, data: DicomData):
        self.selected_channels = []
        self.channels = {}
        log.debug("### Importing RP Data ###")
        for i in range(len(data.channels_rois)):
            channel_number = f"{data.channels_rois[i]}"
            channel_id = f"Channel {data.channels_labels[i]}"
            points = data.channel_paths[i]

            # to print the list of points without quotes
            points_list = f"Raw points: {points}"
            log.debug(points_list.replace("'", ""))

            needle = NeedleChannel(
                number=channel_number, 
                label=channel_id, 
                points=points)
            self.channels[needle.label]= needle
        self.update()

    def on_view_changed(self):
        self.selected_channels = []
        self.update()

    def set_diameter(self, diameter: float):
        for i in range(len(self.channels)):
            self.channels[i].setDiameter(diameter)  # set diameter and calculate shape
        self.update()

    def set_selected_channels(self, *args):
        log.debug(f"setting selected channels")
        self.selected_channels =[]
        if len(args) < 1: raise ValueError("no arguements made!")
        
        # if using indexes to match to the channel's label
        if type(args[0]) is type(int):  # index of the selected channel(s)
            channels = [channel.label for channel in self.channels.values()]
            for index in args:
                self.selected_channels.append(channels[index])
            self.update()
            return None

        elif type(args[0] is type(str)):  # label of selected channel
            self.selected_channels = args
            self.update()
            return None
        
        else:
            raise ValueError(f"wrong value type {type(args[0])}")
    
    def set_selected_shapes(self, *args):
        log.debug(f"setting selected shapes")
        self.selected_channels =[]
        for compound in args[0]:
            for label, needle in self.channels.items():
                if compound.IsEqual(needle.shape()):
                    self.selected_channels.append(label)
                    break
        self.update()

    def set_tandem(self, label:str) -> None:
        self.tandem_channel = label
        self.update()

    def update(self):
        self.values_changed.emit()
        self.update_display()

    def update_display(self):
        shapes = [ShapeModel(
            label=channel.label,
            shape=channel.shape(),
            shape_type=ShapeTypes.CHANNEL
        ) for channel in self.channels.values()]

        # set selected shapes
        for shape in shapes:
            shape.selected = shape.label in self.selected_channels

        app = get_app()
        app.window.displaymodel.add_shapes(shapes)

    def update_height_offset(self, height_offset: float):
        log.debug(f"updating channels height offset")
        for channel in self.channels.values():
            new_channel = channel
            new_channel.set_offset(height_offset)
            self.channels[channel.label] = new_channel
        self.update()

    def __init__(self):
        super().__init__()
        self.channels = {}
        self.diameter = NeedleChannel.default_diameter()
        self.selected_channels = []
        self.tandem_channel = None  # a label for the specified channel to represent the tandem
        self.disabled_channels = []
        
        get_app().signals.viewChanged.connect(self.on_view_changed)

    @staticmethod
    def get_label(): return CHANNELS_LABEL
