from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMainWindow

from Presentation.MainWindow.core import MainWindow

class ImportFunctions(MainWindow):
    # https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html?highlight=qstringlist
    def get_dicom_rs_file(self) -> str:
        filename = QFileDialog.getOpenFileName(self, 'Open Patient RS File', '', "DICOM files (*.dcm)")
        self.ui.files_list.addItem(filename[0])

class ImportDragFunctions(QListWidget):
    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore() 
    
    def drag_move_event(self, event):
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore() 

    def drop(self, event):
        print()
        if event.mimeData().hasUrls():
            event.setDropAction(Qt.CopyAction)
            event.accept()
            
            list = []
            print(event.mimeData().urls())
        else:
            event.ignore() 