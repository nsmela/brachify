import pydicom
import numpy as np

from Core.Models.Cylinder import BrachyCylinder


def read_cylinder_file(filepath):
    # cylinder info
    #   origin is the middle point in the cylinder contour in ROIContourSequence
    #   Referenced ROI Number is found in RT ROI Observations Sequence with the ROI Observation Label contains Surface
    #   use that to get the right contour sequence -> contour data -> list of 3D points
    #   the origin is used as an offset for the rest of the channels for positional accuracy

    dataset = pydicom.read_file(filepath)

    # finding the contour data
    referenced_roi = list(filter(lambda s: ("surface" in s.ROIObservationLabel.lower()),
                                 dataset.RTROIObservationsSequence))[0].ReferencedROINumber
    contour_data = list(filter(lambda s: (s.ReferencedROINumber == referenced_roi),
                               dataset.ROIContourSequence))[0].ContourSequence[0].ContourData

    vals = np.asarray(contour_data)
    numpts = int(len(vals) / 3)
    vals = np.reshape(vals, (numpts, 3))
    xs = vals[:, 0]
    ys = vals[:, 1]
    zs = vals[:, 2]

    # radius
    radius = np.sqrt((xs[-1] - xs[0]) ** 2 + (ys[-1] - ys[0]) ** 2 + (zs[-1] - zs[0]) ** 2) / 2

    tipidx = np.floor(len(xs) / 2)
    tipidx = int(tipidx)
    tip = [xs[tipidx], ys[tipidx], zs[tipidx]]

    baseX = (xs[-1] + xs[0]) / 2
    baseY = (ys[-1] + ys[0]) / 2
    baseZ = (zs[-1] + zs[0]) / 2
    base = [baseX, baseY, baseZ]

    cyl_vec = np.array(tip) - np.array(base)

    return BrachyCylinder(tip, base, radius, True)