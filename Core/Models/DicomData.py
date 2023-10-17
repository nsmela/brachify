class DicomData:
    def __init__(self):
        self.patient_name = None
        self.patient_id = None

        self.cylinder_roi = None
        self.cylinder_color = None
        self.cylinder_contour = None

        self.channels_rois = None
        self.channels_colors = None
        self.channel_contours = None

    def update(self, new_data):
        if new_data.patient_name:
            self.patient_name = new_data.patient_name

        if new_data.patient_id:
            self.patient_id = new_data.patient_id

        if new_data.cylinder_roi :
            self.cylinder_roi = new_data.cylinder_roi

        if new_data.cylinder_color:
            self.cylinder_color = new_data.cylinder_color

        if new_data.cylinder_contour:
            self.cylinder_contour = new_data.cylinder_contour

        if new_data.channels_rois:
            self.channels_rois = new_data.channels_rois

        if new_data.channels_colors:
            self.channels_colors = new_data.channels_colors

        if new_data.channel_contours:
            self.channel_contours = new_data.channel_contours

    def toString(self):
        text = "## DicomData Object:\n"
        text += f"Patient {self.patient_name} -- ID: {self.patient_id}\n"

        if self.cylinder_roi:
            text += f"Cylinder ROI Number {self.cylinder_roi}\n Cylinder Color {self.cylinder_color}\n"
            text += f" Points: {self.cylinder_contour}\n"
        else:
            text += "No Cylinder Data!\n"

        if self.channels_rois:
            text += f"\nChannels ({len(self.channels_rois)} loaded)\n"
            for i in range(len(self.channels_rois)):
                text += f" Channel {self.channels_rois[i]}\n"
                text += f" Channel Color {self.channels_colors[i]}\n"
                text += f" Points: \n"
                for point in self.channel_contours[i]:
                    text += f"  {point}\n"
        else:
            text += "\nNo Channel Data!\n"

        return text

