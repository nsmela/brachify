
class NeedleChannel:
    def __init__(self, number: str, id: str, points):
        self.channelNumber = number
        self.channelId = id
        self.points = points
        self.rawPoints = points
        self.isExtended = False
        self.curve_downwards = 0

    def toDict(self):
        return {"Channel Number": self.channelNumber, "Channel ID": self.channelId, "Points": self.points}
    
    def toString(self):
        return f"Channel {self.channelId} ({self.channelId}: Offset: {self.curve_downwards})"

        