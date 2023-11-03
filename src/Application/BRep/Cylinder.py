from src.Core.Models.Cylinder import BrachyCylinder
from src.Core.Models.DicomData import DicomData

import numpy as np


def get_brachy_cylinder(data: DicomData) -> BrachyCylinder:
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
