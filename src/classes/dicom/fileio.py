import numpy as np
from pathlib import Path

import pydicom

from classes.logger import log
from classes.dicom.data import DicomData
from classes.mesh.cylinder import BrachyCylinder
from classes.mesh.channel import NeedleChannel


def read_dicom_folder(folder_path: str):
        """Used to import a folder, check it for relevant dicom files, and set up the app for the data"""
        files = [ p for p in Path(folder_path).glob('**/*.dcm') if p.is_file()]

        log.debug(f"Found {files} in {folder_path}")

        # look for planning file first
        rp_file = None
        for file in files:
            if is_rp_file(file):
                rp_file = file
                break

        if not rp_file:  # if none of the files within the folder are a rp file
            log.info(f"No rs files where found at {folder_path}")

        # looking for the structure file
        rs_file = None
        for file in files:
            if is_rs_file(file):
                rs_file = file
                break

        if not rs_file:
            log.info(f"No rs file was found in {folder_path}")

        # get data from files
        log.debug(f"Planning file is: {rp_file}")
        log.debug(f"Structure file is: {rs_file}")

        return load_dicom_data(rp_file, rs_file)


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
        log.info(f"Invalid RS DICOM file: {filepath}\n{error_message}")
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
        log.info(f"Invalid RP DICOM file: {filepath} \n{error_message}")
        return False
    else:
        return True


def load_dicom_data(rp_file: str, rs_file: str) -> DicomData:
    data = DicomData()

    try:
        # we use the Planning file to get the channel ROI numbers
        rp_dataset = pydicom.read_file(rp_file)
        data.channels_rois = [
            roi.ReferencedROINumber for roi in rp_dataset.ApplicationSetupSequence[0].ChannelSequence]
        data.channels_labels = [
            roi.SourceApplicatorID for roi in rp_dataset.ApplicationSetupSequence[0].ChannelSequence]
    except Exception as error_message:
        log.error(f"Loading RP Dicom file failed! {rp_file}\n{error_message}")

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

        # cylinder offsets
        point1 = np.asarray(data.cylinder_contour[0])
        point2 = np.asarray(data.cylinder_contour[-1])
        difference = point2 - point1
        diameter = np.sqrt((difference[0]) ** 2 +
                        (difference[1]) ** 2 + (difference[2]) ** 2)
        diameter = round(diameter, 1)

        middle_index = int(len(data.cylinder_contour) / 2)
        data.cylinder_tip = data.cylinder_contour[middle_index]

        data.cylinder_base = point1 + (difference / 2)

        # channels info
        if data.channels_rois:
            channel_contours = list(filter(lambda sequence: (sequence.ReferencedROINumber in data.channels_rois),
                                           rs_dataset.ROIContourSequence))
            data.channels_colors = [
                contour.ROIDisplayColor for contour in channel_contours]

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
        log.error(f"Loading RS Dicom file failed! {rs_file}\n{error_message}")

    log.debug(f"{data.toString()}")
    return data


def dicomCylinder(data: DicomData) -> BrachyCylinder:
    point1 = np.asarray(data.cylinder_contour[0])
    point2 = np.asarray(data.cylinder_contour[-1])
    difference = point2 - point1
    diameter = np.sqrt((difference[0]) ** 2 +
                       (difference[1]) ** 2 + (difference[2]) ** 2)
    diameter = round(diameter, 1)

    middle_index = int(len(data.cylinder_contour) / 2)
    tip = data.cylinder_contour[middle_index]

    base = point1 + (difference / 2)
    log.debug(f"Cylinder results: \n Diameter: {diameter}\n Tip: {tip}\n Base: {base}")
    return BrachyCylinder(tip=tip, base=base, diameter=diameter)


def load_channels(data: DicomData) -> list[NeedleChannel]:
    channels = []
    log.debug("### Importing RP Data ###")
    for i in range(len(data.channels_rois)):
        channel_number = f"{data.channels_rois[i]}"
        channel_id = f"Channel {data.channels_labels[i]}"
        points = data.channel_contours[i]

        log.debug(f" Raw Points: \n{points}\n\n")
        needle = NeedleChannel(number=channel_number,
                               id=channel_id, points=points)
        channels.append(needle)
    return channels
     