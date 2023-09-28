from PyQt5.QtWidgets import QFileDialog, QMainWindow

from Presentation.MainWindow.core import MainWindow

class ImportFunctions(MainWindow):
    # https://srinikom.github.io/pyside-docs/PySide/QtGui/QFileDialog.html?highlight=qstringlist
    def get_dicom_rs_file(self) -> str:
        filename = QFileDialog.getOpenFileName(self, 'Open Patient RS File', '', "DICOM files (*.dcm)")
        self.ui.files_list.insertItem(len(self.files), filename[0])
        # window.files.append(filename[0])