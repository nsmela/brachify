import numpy as np
import math


def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))


def length(v):
  return math.sqrt(dotproduct(v, v))


def get_angle(v1, v2):
  return math.atan2(v2[1] - v1[1], v2[0] - v1[0])


class NeedleChannel:
    def __init__(self, number: str, id: str, points):
        self.channelNumber = number
        self.channelId = id
        self.points = points
        self.rawPoints = points
        self.isExtended = False
        self.curve_downwards = 0
        self.disabled = False
        self.shape = None

    def toDict(self):
        return {"Channel Number": self.channelNumber, "Channel ID": self.channelId, "Points": self.points}
    
    def toString(self):
        return f"Channel {self.channelId} ({self.channelId}: Offset: {self.curve_downwards})"

    # ref: 
    # https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    # https://stackoverflow.com/questions/42258637/how-to-know-the-angle-between-two-vectors
    def getRotation(self):
        # calculate the sin angle on the xy plane using 0,0 and the highest point in the list of points
        v1 = [1.0, 0.0, self.points[0][2]]
        v2 = self.points[0]
        angle = get_angle(v1, v2) * 180 / 3.14159 # convert to degrees
        print(f"needle channel angle: {self.points[0]} : {angle}")

        # ensuring the angle stays between 0 and 360 degrees
        while angle < 0:
            angle += 360
            print(f"Small Angle! corrected to {angle}")

        while angle > 360:
            angle -= 360
            print(f"Large angle! corrected to {angle}")

        return angle


