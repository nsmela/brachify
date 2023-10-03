
class NeedleChannel:
    def __init__(self, number: str, id: str, points, diameter: float = 3.0):
        self.channelNumber = number
        self.channelId = id
        self.points = points
        self.rawPoints = points
        self.diameter = diameter

    def toDict(self):
        return {"Channel Number": self.channelNumber, "Channel ID": self.channelId, "Points": self.points}

        