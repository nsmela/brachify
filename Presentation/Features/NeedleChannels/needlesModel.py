from PyQt5 import QtCore
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse

# https://www.pythonguis.com/tutorials/modelview-architecture/
class NeedlesModel(QtCore.QAbstractListModel):
    def __init__(self, *args, channels = None, **kwargs):
        super(NeedlesModel, self).__init__(*args, **kwargs)
        self.channels = channels or []
        self._shape = None

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            channel = self.channels[index.row()]
            return channel.channelId
    
    def rowCount(self, index):
        return len(self.channels)

    def shape(self):
        if self._shape:
            return self._shape

        shapes = [channel.shape() for channel in self.channels]
        shape = shapes[0] #  priming the fused shapes
        for i in range(1, len(shapes)):
            if self.channels[i].disabled:
                continue
            shape = BRepAlgoAPI_Fuse(shape, shapes[i]).Shape()

        self._shape = shape
        return self._shape