from PyQt5.QtWidgets import QFileDialog
from Presentation.MainWindow.core import MainWindow


def load_tandems(window: MainWindow) -> None:
    '''reads the json file for locally stored tandems and convert it into a list of tandems and store it globally'''
    pass


def save_tandem(window: MainWindow) -> bool:
    '''attempts to add or update the json file containing the tandem settings'''
    pass


def load_tandem_display_model(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Select Tandem Display Model', '', "Supported files (*.stl *.3mf *.obj *.stp *.step)")[0]
    if len(filename) == 0:
        return
    
    window.ui.tandem_lineEdit_displayModel.setText(filename)


def load_tandem_tool_model(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Select Tandem Tool Model', '', "Supported files (*.stl *.3mf *.obj *.stp *.step)")[0]
    if len(filename) == 0:
        return
    
    window.ui.tandem_lineEdit_toolModel.setText(filename)


def clear_tandem_settings(window: MainWindow) -> None:
    window.ui.tandem_lineEdit_displayModel.setText("")
    window.ui.tandem_lineEdit_toolModel.setText("")
    window.ui.lineEdit_tandemName.setText("")
    window.ui.spinBox_tandem_xOffset.setValue(0.0)
    window.ui.spinBox_tandem_yOffset.setValue(0.0)
    window.ui.spinBox_tandem_zOffset.setValue(0.0)
    window.ui.btn_tandem_add_update.setObjectName("Add")