# the raw dicom data and how to grab relevant data from it
import pydicom
import numpy as np

from core.dicom_data import DicomData
from core.needle import Needle


def _convert_contours_to_points(contour_data):
    points = []
    while len(contour_data) > 0:
        x = contour_data.pop()
        y = contour_data.pop()
        z = contour_data.pop()
        point = np.array([x, y, z])
        points.append(point)
    return points


def _convert_control_point(brachy_control_point) -> np.array:
    position = brachy_control_point.ControlPoint3DPosition
    point = np.array([position[0], position[1], position[2]])
    return point


def _read_cylinder_origin(dataset):
    # cylinder info
    #   origin is the middle point in the cylinder contour in ROIContourSequence
    #   Referenced ROI Number is found in RT ROI Observations Sequence with the ROI Observation Label contains Surface
    #   use that to get the right contour sequence -> contour data -> list of 3D points
    #   the origin is used as an offset for the rest of the channels for positional accuracy

    # finding the contour data
    referenced_roi = list(filter(lambda s:
                                 ("surface" in s.ROIObservationLabel.lower()),
                                 dataset.RTROIObservationsSequence))[0].ReferencedROINumber
    contour_data = list(filter(lambda s:
                               (s.ReferencedROINumber == referenced_roi),
                               dataset.ROIContourSequence))[0].ContourSequence[0].ContourData
    cylinder_outline = np.asarray(contour_data)
    points = _convert_contours_to_points(contour_data)

    # origin
    index = int(len(points) / 2)
    origin = points[index]

    # radius calculated by square root of squared distance between first and last point
    start_point = points[0]
    end_point = points[-1]
    squared_distance = np.sum((start_point - end_point) ** 2, axis=0)
    radius = np.sqrt(squared_distance)

    vals = cylinder_outline
    numpts = int(len(vals) / 3)
    vals = np.reshape(vals, (numpts, 3))
    xs = vals[:, 0]
    ys = vals[:, 1]
    zs = vals[:, 2]

    tipidx = np.floor(len(xs) / 2)
    tipidx = int(tipidx)
    tip = [xs[tipidx], ys[tipidx], zs[tipidx]]

    baseX = (xs[-1] + xs[0]) / 2
    baseY = (ys[-1] + ys[0]) / 2
    baseZ = (zs[-1] + zs[0]) / 2
    base = [baseX, baseY, baseZ]

    return origin, radius, base, tip


def _read_needle_channels(dataset):
    channelSequence = dataset.ApplicationSetupSequence[0].ChannelSequence

    channels = []
    for channel in channelSequence:
        channelNumber = channel.ChannelNumber
        channelID = channel.SourceApplicatorID
        sequence = channel.BrachyControlPointSequence

        # points = []
        # for p in sequence:
        #    points.append(_convert_control_point(p))
        points = [_convert_control_point(p) for p in sequence]

        # removing duplicate points
        del points[::2]

        needle = {
            "Channel Number": channelNumber,
            "Channel ID": channelID,
            "Points": points
        }
        channels.append(needle)
    return channels


def _Rotate_Cloud(Points, V1, V2):
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
    theta = np.arccos(V1V2Dot / (V1Norm * V2Norm))

    # Using Rodrigues' rotation formula (wikipedia):
    e = V1V2CrossNormalized

    pts_rotated = np.empty((len(Points), 3))
    if np.size(Points) == 3:
        p = Points
        p_rotated = np.cos(theta) * p + np.sin(theta) * (np.cross(e, p)) + (1 - np.cos(theta)) * np.dot(e, p) * e
        pts_rotated = p_rotated
    else:
        for i, p in enumerate(Points):
            p_rotated = np.cos(theta) * p + np.sin(theta) * (np.cross(e, p)) + (1 - np.cos(theta)) * np.dot(e, p) * e
            pts_rotated[i] = p_rotated
    return pts_rotated

def get_cylinder_vector(data: DicomData):
    return np.array(data.cylinder_tip) - np.array(data.cylinder_base)

def addRSFile(filepath: str) -> DicomData:
    dataset = pydicom.read_file(filepath)
    origin, radius, base, tip = _read_cylinder_origin(dataset)
    print(origin)
    print(radius)
    print(base)
    print(tip)
    data = DicomData()
    data.cylinder_origin = origin
    data.cylinder_base = base
    data.cylinder_tip = tip
    return data

def addRPFile(filepath: str):
    dataset = pydicom.read_file(filepath)
    channels = _read_needle_channels(dataset)
    needles = []
    for channel in channels:
        needles.append(
            Needle(
                number= channel['Channel Number'],
                id= channel['Channel ID'],
                points= channel['Points']))
    return channels