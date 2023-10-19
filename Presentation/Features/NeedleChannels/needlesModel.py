from PyQt5 import QtCore
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Fuse
from OCC.Core.TopoDS import TopoDS_Shape

# https://www.pythonguis.com/tutorials/modelview-architecture/
class NeedlesModel(QtCore.QAbstractListModel):
    def __init__(self, *args, channels=None, **kwargs):
        super(NeedlesModel, self).__init__(*args, **kwargs)
        self.channels = channels or []
        self._shape = None

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            channel = self.channels[index.row()]
            return channel.channelId

    def rowCount(self, index):
        return len(self.channels)

    def clearShape(self):
        self._shape = None

    def shape(self):
        if self._shape:
            return self._shape

        shapes = [channel.shape() for channel in self.channels]
        shape = None
        for i in range(0, len(shapes)):
            if self.channels[i].disabled:
                continue

            if shape is None:
                shape = shapes[i]
            else:
                shape = BRepAlgoAPI_Fuse(shape, shapes[i]).Shape()

        self._shape = shape
        return self._shape
