# the raw dicom data and how to grab relevant data from it

from Core.Models.Cylinder import BrachyCylinder
from Core.Models.DicomData import DicomData
from Application.NeedleChannels.Models import NeedleChannel

import pydicom
import numpy as np



def is_rs_file(filepath: str) -> bool:
    '''Checks if a file is a RTSTRUCT DICOM file and if it contains the data to make a cylinder'''
    try:
        dataset = pydicom.read_file(filepath)
        #check the type
        if dataset.Modality == 'RTSTRUCT':
            # try to find the contour data
            try:
                referenced_roi = list(filter(lambda s:
                                            ("surface" in s.ROIObservationLabel.lower()),
                                            dataset.RTROIObservationsSequence))[0].ReferencedROINumber
                contour_data = list(filter(lambda s:
                                        (s.ReferencedROINumber == referenced_roi),
                                        dataset.ROIContourSequence))[0].ContourSequence[0].ContourData
            except:
                print("No surface contour")
                
        else:
            return False
    except Exception as error_message:
        print(f"Error reading dicom file: {filepath}\n{error_message}")
        return False
    else:
        return True


def is_rp_file(filepath: str) -> bool:
    '''Checks if a file is a RTPLAN DICOM file and if it contains the data for needle channels'''
    try:
        dataset = pydicom.read_file(filepath)
        #check the type
        try:
            if dataset.Modality == 'RTPLAN':
                # finding the contour data
                channels = dataset.ApplicationSetupSequence[0].ChannelSequence
                if len(channels) < 1:
                    return False
            else:
                return False
        except Exception as error_message:
            print(f"Invalid RP DICOM file: {filepath} \n{error_message}")        
    except Exception as error_message:
        print(f"Error reading RP DICOM file: {filepath} \n{error_message}")
        return False
    else:
        return True


def load_dicom_data(rp_file: str, rs_file: str) -> DicomData:
    data = DicomData()

    # GET THE CHANNEL ROI NUMBERS
    try:
        # we use the Planning file to get the channel ROI numbers
        rp_dataset = pydicom.read_file(rp_file)
        data.channels_rois = [
            roi.ReferencedROINumber for roi in rp_dataset.ApplicationSetupSequence[0].ChannelSequence]
        data.channels_labels = [
            roi.SourceApplicatorID for roi in rp_dataset.ApplicationSetupSequence[0].ChannelSequence]
    except Exception as error_message:
        print(f"Reading RP Dicom file failed! {rp_file}\n{error_message}")

    # CHECK IF A CENTRAL AXIS NEEDLE IS LABELED/USED
    for i, label in enumerate(data.channels_labels):
        for mylabel in ["Central Axis", "centralaxis"]:
            if mylabel.lower() in label.lower():
                data.central_axis_flag = True
                centralaxisrefROINumber = data.channels_rois[i]
                center_index = i
                break

    # IF THERE'S A CENTRAL AXIS, ADD IT TO DATA AND REMOVE IT FROM THE LIST
    if data.central_axis_flag:
        data.central_channel_roi = data.channels_rois[center_index]
        data.channels_labels.pop(center_index)
        data.channels_rois.pop(center_index)

    # GET THE SURFACE GEOMETRY, IF THERE ISN'T A CENTRAL AXIS CHANNEL
    try:
        # We use the RS planning file to get the Applicator's ROI and contour data
        # We also use it to get the channel ROI data if we have their ROIS
        rs_dataset = pydicom.read_file(rs_file)

        if not data.central_axis_flag:
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
                for i in range(0, len(cylinder_contour.ContourSequence[0].ContourData), 3)] #not an efficient way to do this.
        else:
            data.cylinder_color = [0,255,255]
            # might need some more items here

    except Exception as error_message:
        print(f"Loading RS Dicom surface struct or no central axis identified! {rs_file}\n{error_message}")

    # GET THE CHANNEL CONTOUR DATA
    try:
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
        print(f"Loading RS Dicom channel data failed! {rs_file}\n{error_message}")

    # ADD THE CENTRAL CHANNEL CONTOUR POINTS TO THE DATA OBJECT
    try:
        if data.central_axis_flag:
            for sequence in rs_dataset.ROIContourSequence:
                if sequence.ReferencedROINumber == data.central_channel_roi:
                    central_channel = sequence
                    break

            channel_contour_raw = central_channel.ContourSequence[0].ContourData
            points = [channel_contour_raw[i:i + 3] for i in range(0, len(channel_contour_raw), 3)]
            data.central_channel = points

    except Exception as error_message:
        print(f"Loading RS Dicom channel data failed! {rs_file}\n{error_message}")

    try:
        data.patient_name = rp_dataset.PatientName
        data.patient_id = rp_dataset.PatientID
        data.plan_label = rp_dataset.RTPlanLabel
    except Exception as error_message:
        print(f"Loading patient name/ID from RS Dicom file failed! {rs_file}\n{error_message}")

    print(f"{data.toString()}")
    return data


def load_cylinder(data: DicomData) -> BrachyCylinder:
    if data.central_axis_flag:
        tip = data.central_channel[0]
        base = data.central_channel[-1]
        diameter = 30 #hardcoded default. user needs to be flagged...
        print(f"Cylinder results: \n Diameter: {diameter}\n Tip: {tip}\n Base: {base}")
        return BrachyCylinder(tip=tip, base=base, diameter=diameter)

    else:
        point1 = np.asarray(data.cylinder_contour[0])
        point2 = np.asarray(data.cylinder_contour[-1])
        difference = point2 - point1
        diameter = np.sqrt((difference[0]) ** 2 +
                        (difference[1]) ** 2 + (difference[2]) ** 2)
        diameter = round(diameter, 1)

        middle_index = int(len(data.cylinder_contour) / 2)
        tip = data.cylinder_contour[middle_index]

        base = point1 + (difference / 2)
        print(
            f"Cylinder results: \n Diameter: {diameter}\n Tip: {tip}\n Base: {base}")
    return BrachyCylinder(tip=tip, base=base, diameter=diameter)


def load_channels(data: DicomData) -> list[NeedleChannel]:
    channels = []
    print("### Importing RP Data ###")
    for i in range(len(data.channels_rois)):
        channel_number = f"{data.channels_rois[i]}"
        channel_id = f"Channel {data.channels_labels[i]}"
        points = data.channel_contours[i]

        # to print the list fo points without quotes
        points_list = f"Raw points: {points}"
        print(points_list.replace("'", ""))

        needle = NeedleChannel(number=channel_number,
                               id=channel_id, points=points)
        channels.append(needle)
    return channels
