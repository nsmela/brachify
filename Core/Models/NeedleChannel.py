
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

    def getRotation(self):
        # calculate the sin angle on the xy plane using 0,0 and the highest point in the list of points
        # sort by z
        # get xy
        # get angle (radians or degrees?)
        # return result
        pass