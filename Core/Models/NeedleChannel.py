import numpy as np


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

    # ref: https://stackoverflow.com/questions/2827393/angles-between-two-n-dimensional-vectors-in-python/13849249#13849249
    def getRotation(self):
        # calculate the sin angle on the xy plane using 0,0 and the highest point in the list of points
        return angle([0.0, 0.0, self.points[0][2]], self.points[0]) * 180 / 3.14159 # convert to degrees


import math

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
