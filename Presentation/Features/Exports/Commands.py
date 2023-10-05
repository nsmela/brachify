from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMainWindow

from Presentation.MainWindow.core import MainWindow
import Application.Exports.export_stl as exports

class ExportFunctions(MainWindow):
    def export_stl(self) -> None:
            filename = QFileDialog.getSaveFileName(self, 'Save solid as STL', '', "STL files (*.stl)")[0]
            exports.export_stl(filename, self.display_export)