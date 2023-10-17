import numpy as np
import pydicom

from Core.Models.NeedleChannel import NeedleChannel


def _convert_control_point(brachy_control_point):
    position = brachy_control_point.ControlPoint3DPosition
    point = [position[0], position[1], position[2]]
    return point


def read_needles_file(filepath: str):
    dataset = pydicom.read_file(filepath)
     
    channel_sequence = dataset.ApplicationSetupSequence[0].ChannelSequence

    channels = []
    print("### Importing RP File ###")
    for channel in channel_sequence:
        channel_number = channel.ChannelNumber
        channel_id = channel.SourceApplicatorID
        sequence = channel.BrachyControlPointSequence

        points = [_convert_control_point(p) for p in sequence]

        print(f" Raw Points: \n{points}\n\n")
        # removing duplicate points
        del points[::2]
        print(f" Every second point removed: \n{points}\n\n")
        needle = NeedleChannel(number=channel_number, id=channel_id, points=points)
        channels.append(needle)
    return channels


def read_rs_file(filepath: str) -> list:
    dataset = pydicom.read_file(filepath)
    referenced_applicators = list(filter(lambda s: ("applicator" in s.ROIObservationLabel.lower()),
                                 dataset.RTROIObservationsSequence))
    referenced_roi = [roi.ReferencedROINumber for roi in referenced_applicators]
    applicators = list(filter(lambda s: (s.ReferencedROINumber in referenced_roi),
                               dataset.ROIContourSequence))
    print(f"{applicators}")

    return None


def Rotate_Cloud(points, V1, V2):
    # V1 is the current vector which the coordinate system is aligned to
    # V2 is the vector we want the system aligned to
    # Points is an (n,3) array of n points (x,y,z)
    V1 = np.asarray(V1)
    V2 = np.asarray(V2)

    # Normalize V1 and V2 in case they aren't already
    V1Len = (V1[0] ** 2 + V1[1] ** 2 + V1[2] ** 2) ** 0.5
    V2Len = (V2[0] ** 2 + V2[1] ** 2 + V2[2] ** 2) ** 0.5
    V1 = V1 / V1Len
    V2 = V2 / V2Len

    # Calculate the vector cross product
    V1V2Cross = np.cross(V1, V2)
    V1V2CrossNorm = (V1V2Cross[0] ** 2 + V1V2Cross[1] ** 2 + V1V2Cross[2] ** 2) ** 0.5
    V1V2CrossNormalized = V1V2Cross / V1V2CrossNorm

    # Dot product
    V1V2Dot = np.dot(V1, V2)
    V1Norm = (V1[0] ** 2 + V1[1] ** 2 + V1[2] ** 2) ** 0.5
    V2Norm = (V2[0] ** 2 + V2[1] ** 2 + V2[2] ** 2) ** 0.5

    # Angle between the vectors
    Theta = np.arccos(V1V2Dot / (V1Norm * V2Norm))

    # Using Rodrigues' rotation formula (wikipedia):
    e = V1V2CrossNormalized

    pts_rotated = np.empty((len(points), 3))
    if np.size(points) == 3:
        p = points
        p_rotated = np.cos(Theta) * p + np.sin(Theta) * (np.cross(e, p)) + (1 - np.cos(Theta)) * np.dot(e, p) * e
        pts_rotated = p_rotated
    else:
        for i, p in enumerate(points):
            p_rotated = np.cos(Theta) * p + np.sin(Theta) * (np.cross(e, p)) + (1 - np.cos(Theta)) * np.dot(e, p) * e
            pts_rotated[i] = p_rotated
    return pts_rotated
