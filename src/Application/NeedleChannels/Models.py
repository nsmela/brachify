from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Extend.ShapeFactory import translate_shp

from src.Application.BRep.Channel import *
from src.Core.Models.NeedleChannel import NeedleChannelModel

import math


class NeedleChannel(NeedleChannelModel):
    def __init__(self, number: str, id: str, points):
        super().__init__(number, id, points)
        self.disabled = False
        self.isIntersecting = False
        self._shape = None
        self._offset = 0.0
        self._diameter = 3.0

    def shape(self) -> TopoDS_Shape:
        if self._shape:
            return self._shape

        self._shape = rounded_channel(
            self.points, self._offset, self._diameter)
        #  self._shape = generate_curved_channel(self.points, self._offset, self._diameter)
        return self._shape

    def setChannel(self, height: float = 0.0, diameter: float = 3.0) -> None:
        self._offset = height
        self._diameter = diameter
        self._shape = None
        self.shape()

    def setDiameter(self, diameter: float) -> None:
        self._diameter = diameter
        self._shape = None
        self.shape()

    def setOffset(self, height: float = 0.0) -> None:
        self._offset = height
        self._shape = None
        self.shape()

    def getDiameter(self):
        return self._diameter

    def getOffset(self) -> float:
        return self._offset

    # ref:
    # https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    # https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors
    def getRotation(self):
        # calculate the sin angle on the xy plane using 0,0 and the highest point in the list of points
        v1 = [1.0, 0.0, self.points[0][2]]
        v2 = self.points[0]
        angle = math.atan2(v2[1] - v1[1], v2[0] - v1[0]) * \
            (180 / 3.14159)  # convert to degrees
        print(f"needle channel angle: {self.points[0]} : {angle}")

        # ensuring the angle stays between 0 and 360 degrees
        while angle < 0:
            angle += 360
            print(f"Small Angle! corrected to {angle}")

        while angle > 360:
            angle -= 360
            print(f"Large angle! corrected to {angle}")

        return angle
