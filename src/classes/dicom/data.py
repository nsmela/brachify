class DicomData:
    """
    Stores relevant data from a dicom dataset
    """

    def __init__(self):
        self.patient_name = None
        self.patient_id = None
        self.plan_label = None

        self.cylinder_roi = None
        self.cylinder_contour = None
        self.cylinder_tip = None
        self.cylinder_base = None
        self.cylinder_direction = None
        self.cylinder_diameter = None

        self.central_channel_roi = None

        self.channels_rois = None
        self.channels_labels = None
        self.channel_contours = None
        self.channel_paths = None

        self.central_channel_roi = False
        self.central_axis_flag = None
        self.central_channel = None

    def update(self, new_data):
        if new_data.patient_name:
            self.patient_name = new_data.patient_name

        if new_data.patient_id:
            self.patient_id = new_data.patient_id

        if new_data.plan_label:
            self.plan_label = new_data.plan_label

        if new_data.cylinder_roi:
            self.cylinder_roi = new_data.cylinder_roi

        if new_data.cylinder_contour:
            self.cylinder_contour = new_data.cylinder_contour

        if new_data.channels_rois:
            self.channels_rois = new_data.channels_rois

        if new_data.channel_contours:
            self.channel_contours = new_data.channel_contours

    def toString(self):
        text = "## DicomData Object:\n"
        text += f"Patient {self.patient_name} -- ID: {self.patient_id}\n"

        if self.cylinder_roi:
            text += f"Cylinder ROI Number {self.cylinder_roi}\n"
        else:
            text += "No Cylinder Data!\n"

        if self.channels_rois:
            text += f"\nChannels ({len(self.channels_rois)} loaded)\n"
            for i in range(len(self.channels_rois)):
                text += f" Channel {self.channels_rois[i]}\n"
        else:
            text += "\nNo Channel Data!\n"

        return text

    def toJson(self) -> dict:
        return {
            "Patient Name": self.patient_name,
            "Patient ID": self.patient_id,
            "Plan Label": self.plan_label,
            "Cylinder ROI": self.cylinder_roi,
            "Cylinder Contour": self.cylinder_contour,
            "Channel ROIs": self.channels_rois,
            "Channel Labels": self.channels_labels,
            "Channel Contours": self.channel_contours
        }

    def fromJson(self, json: dict) -> None:
        self.patient_name = json["Patient Name"]
        self.patient_id = json["Patient ID"]
        self.plan_label = json["Plan Label"]
        self.cylinder_roi = json["Cylinder ROI"]
        self.cylinder_contour = json["Cylinder Contour"]
        self.channels_rois = json["Channel ROIs"]
        self.channels_labels = json["Channel Labels"]
        self.channel_contours = json["Channel Contours"]
