import math


class NeedleChannelModel:
    def __init__(self, number: str, id: str, points):
        self.channelNumber = number
        self.channelId = id
        self.points = points
        self.rawPoints = points
