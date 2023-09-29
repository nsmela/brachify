
class NeedleChannel:
    def __init__(self, number: str, id: str, points):
        self.channelNumber = number
        self.channelId = id
        self.points = points
        self.rawPoints = points

    def toDict(self):
        return {"Channel Number": self.channelNumber, "Channel ID": self.channelId, "Points": self.points}

        