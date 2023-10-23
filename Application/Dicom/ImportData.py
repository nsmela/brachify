from Core.Models.Cylinder import BrachyCylinder
from Core.Models.DicomData import DicomData
from Application.NeedleChannels.Models import NeedleChannel

import pydicom
import numpy as np


def is_rs_file(filepath: str) -> bool:
    """Checks if a file is a DICOM file and if it contains the data to make a cylinder"""
    try:
        dataset = pydicom.read_file(filepath)
        # finding the contour data
        referenced_roi = list(filter(lambda s:
                                     ("surface" in s.ROIObservationLabel.lower()),
                                     dataset.RTROIObservationsSequence))[0].ReferencedROINumber
        contour_data = list(filter(lambda s:
                                   (s.ReferencedROINumber == referenced_roi),
                                   dataset.ROIContourSequence))[0].ContourSequence[0].ContourData
    except Exception as error_message:
        print(f"Invalid RS DICOM file: {filepath}\n{error_message}")
        return False

    return True


def is_rp_file(filepath: str) -> bool:
    """Checks if a file is a DICOM file and if it contains the data for needle channels"""
    try:
        dataset = pydicom.read_file(filepath)
        # finding the contour data
        channels = dataset.ApplicationSetupSequence[0].ChannelSequence
        if len(channels) < 1:
            return False
    except Exception as error_message:
        print(f"Invalid RP DICOM file: {filepath} \n{error_message}")
        return False
    else:
        return True


def load_dicom_data(rp_file: str, rs_file: str) -> DicomData:
    data = DicomData()

    try:
        # we use the Planning file to get the channel ROI numbers
        rp_dataset = pydicom.read_file(rp_file)
        data.channels_rois = [roi.ReferencedROINumber for roi in rp_dataset.ApplicationSetupSequence[0].ChannelSequence]
        data.channels_labels = [roi.SourceApplicatorID for roi in rp_dataset.ApplicationSetupSequence[0].ChannelSequence]
    except Exception as error_message:
        print(f"Loading RP Dicom file failed! {rp_file}\n{error_message}")

    try:
        # We use the RS file to get the Applicator's ROI and contour data
        # We also use it to get the channel ROI data if we have their ROIS
        rs_dataset = pydicom.read_file(rs_file)

        # cylinder info
        data.cylinder_roi = list(filter(lambda s: ("surface" in s.ROIObservationLabel.lower()),
                                        rs_dataset.RTROIObservationsSequence))[0].ReferencedROINumber
        cylinder_contour = list(filter(lambda s: (s.ReferencedROINumber == data.cylinder_roi),
                                       rs_dataset.ROIContourSequence))[0]
        data.cylinder_color = cylinder_contour.ROIDisplayColor

        data.cylinder_contour = [[
            cylinder_contour.ContourSequence[0].ContourData[i],
            cylinder_contour.ContourSequence[0].ContourData[i + 1],
            cylinder_contour.ContourSequence[0].ContourData[i + 2]]
            for i in range(0, len(cylinder_contour.ContourSequence[0].ContourData), 3)]

        # channels info
        if data.channels_rois:
            channel_contours = list(filter(lambda sequence: (sequence.ReferencedROINumber in data.channels_rois),
                                           rs_dataset.ROIContourSequence))
            data.channels_colors = [contour.ROIDisplayColor for contour in channel_contours]

            # channel points are a single array dividable by 3
            # so for each channel, take those three points and put them into a small 3 list
            channel_contour_points = []
            for channel in channel_contours:
                points = [[
                    channel.ContourSequence[0].ContourData[i],
                    channel.ContourSequence[0].ContourData[i + 1],
                    channel.ContourSequence[0].ContourData[i + 2]]
                    for i in range(0, len(channel.ContourSequence[0].ContourData), 3)
                ]
                channel_contour_points.append(points)
            data.channel_contours = channel_contour_points

    except Exception as error_message:
        print(f"Loading RS Dicom file failed! {rs_file}\n{error_message}")

    print(f"{data.toString()}")
    return data


def dicomCylinder(data: DicomData) -> BrachyCylinder:
    point1 = np.asarray(data.cylinder_contour[0])
    point2 = np.asarray(data.cylinder_contour[-1])
    difference = point2 - point1
    diameter = np.sqrt((difference[0]) ** 2 + (difference[1]) ** 2 + (difference[2]) ** 2)
    diameter = round(diameter, 1)

    middle_index = int(len(data.cylinder_contour) / 2)
    tip = data.cylinder_contour[middle_index]

    base = point1 + (difference / 2)
    print(f"Cylinder results: \n Diameter: {diameter}\n Tip: {tip}\n Base: {base}")
    return BrachyCylinder(tip=tip, base=base, diameter=diameter)


def load_channels(data: DicomData) -> list[NeedleChannel]:
    channels = []
    print("### Importing RP Data ###")
    for i in range(len(data.channels_rois)):
        channel_number = f"{data.channels_rois[i]}"
        channel_id = f"Channel {data.channels_labels[i]}"
        points = data.channel_contours[i]

        print(f" Raw Points: \n{points}\n\n")
        needle = NeedleChannel(number=channel_number, id=channel_id, points=points)
        channels.append(needle)
    return channels
