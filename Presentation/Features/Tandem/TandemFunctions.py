from PyQt5.QtWidgets import QFileDialog

from Presentation.MainWindow.core import MainWindow
import Presentation.Features.Imports.ImportFunctions as imports 
from Core.Models.Tandem import TandemModel

import os
import json
import shutil


tandem_dir = ".\\files\\tandem"
data_filepath = os.path.join(tandem_dir, "tandem.json")


def load_tandems(window: MainWindow) -> None:
    '''reads the json file for locally stored tandems and convert it into a list of tandems and store it globally'''
    window.ui.listWidget_savedTandems.clear()
    
    try:
        with open(data_filepath, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError as error_message:
        print(f"File {data_filepath} was not found! \n {error_message}")

    if data is None: 
        return

    for tandem in data:
        window.ui.listWidget_savedTandems.addItem(tandem)
    


def save_tandem(window: MainWindow) -> bool:
    '''attempts to add or update the json file containing the tandem settings'''
    tandem_name = window.ui.lineEdit_tandemName.text()
    tandem_display_model = window.ui.tandem_lineEdit_displayModel.text()
    tandem_tool_model = window.ui.tandem_lineEdit_toolModel.text()
    tandem_offsets = [
            window.ui.spinBox_tandem_xOffset.value(),
            window.ui.spinBox_tandem_yOffset.value(),
            window.ui.spinBox_tandem_zOffset.value()]
    
    # check if info is enough to proceed
    if not tandem_name:
        return
    if not tandem_display_model:
        return
    if not tandem_tool_model:
        return

    # turn info into dict for json
    tandem = TandemModel()
    tandem.name = tandem_name
    tandem.shape_filepath = os.path.join(tandem_dir, f"{tandem_name}_display{os.path.splitext(tandem_display_model)[1]}")
    tandem.tool_filepath = os.path.join(tandem_dir, f"{tandem_name}_tool{os.path.splitext(tandem_tool_model)[1]}")
    tandem.offsets = tandem_offsets
    
    # check if file exists, if not create a blank one
    try:
        # load file if exists
        with open(data_filepath, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # if not, save the info instead
        # copy model files to the tandem directory
        result = shutil.copy(tandem_display_model, tandem.shape_filepath)
        print(f"diaply model copied to {result}")

        result = shutil.copy(tandem_tool_model, tandem.tool_filepath)
        print(f"tool model copied to {result}")
        
        data = tandem.toDict()
        with open(data_filepath, "x") as data_file:
            json.dump(data, data_file, indent=4)
    except:
        print("Tandem save failed!")
        return
    else:
        # copy model files to the tandem directory
        result = shutil.copy(tandem_display_model, tandem.shape_filepath)
        print(f"diaply model copied to {result}")

        result = shutil.copy(tandem_tool_model, tandem.tool_filepath)
        print(f"tool model copied to {result}")
        
        data.update(tandem.toDict())
        with open(data_filepath, "w") as data_file:
            json.dump(data, data_file, indent=4)
    finally:
        load_tandems(window)


def set_tandem(window: MainWindow, index:int) -> None:
    with open(data_filepath, "r") as data_file:
        data = json.load(data_file)
    
    print(data)
    selection = list(data)[index]
    selection = data[selection]
    print(selection)

    tandem = TandemModel()
    tandem.fromDict(selection)
    
    print(tandem.toDict())
    window.tandem = tandem
    load_tandem_models(window)


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


def load_tandem_models(window: MainWindow) -> None:
    tandem = window.tandem
    
    if not tandem:
        return
    
    if not os.path.exists(tandem.shape_filepath):
        print(f"Tandem {tandem.name} display model is referencing an invalid filepath: {tandem.shape_filepath}")
        return

    if not os.path.exists(tandem.tool_filepath):
        print(f"Tandem {tandem.name} tool model is referencing an invalid filepath: {tandem.tool_filepath}")
        return
    
    tandem.shape = imports.import_step(tandem.shape_filepath)
    tandem.tool_shape = imports.import_step(tandem.tool_filepath)
    
    from Presentation.MainWindow.ui_functions import UIFunctions
    UIFunctions.setPage(window, 3)