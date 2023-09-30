from PyQt5 import QtCore

# https://www.pythonguis.com/tutorials/modelview-architecture/
class NeedlesModel(QtCore.QAbstractListModel):
    def __init__(self, *args, channels = None, **kwargs):
        super(NeedlesModel, self).__init__(*args, **kwargs)
        self.channels = channels or []

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            number, id, points = self.channels[index.row()]
            return id
    
    def rowCount(self, index):
        return len(self.channels)