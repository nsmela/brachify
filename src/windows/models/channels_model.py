from PySide6.QtCore import QObject, Signal

from classes.app import get_app
from classes.dicom.data import DicomData
from classes.mesh.channel import NeedleChannel
from classes.logger import log
from windows.models.shape_model import ShapeModel

CHANNELS_LABEL = "applicator_"

CYLINDER_COLOUR = [0.0, 0.0, 0.0]
TANDEM_COLOUR = [0.0, 0.0, 0.0]
CHANNEL_COLOUR_STANDARD = [0.2, 0.55, 0.55]
CHANNEL_COLOUR_ACTIVE = [0.2, 0.95, 0.55]
CHANNEL_COLOUR_COLLIDING = [0.95, 0.1, 0.1]
CHANNEL_COLOUR_DISABLED = [0.05, 0.05, 0.05]

class ChannelsModel(QObject):

    values_changed = Signal()

    # Slotted to Dicom Model's update
    def load_data(self, data: DicomData):
        self.channels = []
        log.debug("### Importing RP Data ###")
        for i in range(len(data.channels_rois)):
            channel_number = f"{data.channels_rois[i]}"
            channel_id = f"Channel {data.channels_labels[i]}"
            points = data.channel_paths[i]

            # to print the list fo points without quotes
            points_list = f"Raw points: {points}"
            log.debug(points_list.replace("'", ""))

            needle = NeedleChannel(number=channel_number, label=channel_id, points=points)
            self.channels.append(needle)
        self.values_changed.emit()
        self.update_display()

    def update(self):
        self.values_changed.emit()
        self.update_display()

    def update_display(self):
        shapes = [ShapeModel(
            label=f"{CHANNELS_LABEL}{channel.number}",
            shape=channel.shape()
        ) for channel in self.channels]

        app = get_app()
        app.window.displaymodel.add_shapes(shapes)

    def update_height_offset(self, height_offset: float):
        log.debug(f"updating channels height offset")
        pass

    def __init__(self):
        super().__init__()
        self.channels = []