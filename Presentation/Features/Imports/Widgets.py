from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QListWidget

# https://www.youtube.com/watch?v=7hbL0ztIYCg

class ListWidget(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event) -> None:
        if event.mineData().hasUrls():
            event.accept()       
        else:
            event.ignore()

    def dragMoveEvent(self, event) -> None:
        if event.mineData().hasUrls():
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()       
        else:
            event.ignore()

    def dropEvent(self, event):
        #if event.mineData().hasUrls():
        event.setDropAction(QtCore.Qt.CopyAction)
        event.accept()
            
        items = []
        print(event.mineData().urls())