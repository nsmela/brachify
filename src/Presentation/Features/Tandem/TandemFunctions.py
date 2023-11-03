from PySide6.QtWidgets import QFileDialog

from src.Application.Tandem.Models import Tandem
from src.Presentation.MainWindow.core import MainWindow
import src.Presentation.Features.Imports.ImportFunctions as imports
import src.Presentation.Features.Tandem.TandemDisplay as tandemDisplay
from src.Core.Models.Tandem import TandemModel

import os
import json
import shutil

DEFAULT_DIR = os.path.join(os.getcwd() + "\\files", "tandem")
DEFAULT_FILEPATH = os.path.join(DEFAULT_DIR, "tandem.json")
DEFAULT_ROTATION = 0.0

tandem_height = -30.0


def load_tandems(window: MainWindow) -> None:
    """reads the json file for locally stored tandems and convert it into a list of tandems and store it globally"""
    window.ui.listWidget_savedTandems.clear()

    try:
        with open(DEFAULT_FILEPATH, "r") as data_file:
            window.tandems = json.load(data_file)
    except FileNotFoundError as error_message:
        print(f"File {DEFAULT_FILEPATH} was not found! \n {error_message}")
        if not os.path.exists(DEFAULT_DIR):
            os.makedirs(DEFAULT_DIR)

    if window.tandems is None:
        return

    for tandem in window.tandems:
        window.ui.listWidget_savedTandems.addItem(tandem)

    set_tandem(window)


def save_tandem(window: MainWindow) -> bool:
    """attempts to add or update the json file containing the tandem settings"""
    tandem_name = window.ui.lineEdit_tandemName.text()
    tandem_model = window.ui.tandem_lineEdit_toolModel.text()
    index = window.ui.listWidget_savedTandems.currentRow()

    # check if info is enough to proceed
    if not tandem_name:
        return False
    if not tandem_model:
        return False

    # turn info into dict for json
    tandem = TandemModel()
    tandem.name = tandem_name
    tandem.shape_filepath = os.path.join(DEFAULT_DIR, f"{tandem_name}_model{os.path.splitext(tandem_model)[1]}")

    # check if file exists, if not create a blank one
    try:
        # load file if exists
        with open(DEFAULT_FILEPATH, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # if not, save the info instead
        # copy model files to the tandem directory
        result = shutil.copy(tandem_model, tandem.shape_filepath)
        print(f"tandem model copied to {result}")

        data = tandem.toDict()
        with open(DEFAULT_FILEPATH, "x") as data_file:
            json.dump(data, data_file, indent=4)
    except Exception as error_message:
        print(f"Tandem save failed: {error_message}")
        return False
    else:
        # copy model file to the tandem directory
        try:
            result = shutil.copy(tandem_model, tandem.shape_filepath)
            print(f"display model copied to {result}")
        except shutil.SameFileError as error_message:
            print(f"File {tandem.shape_filepath} already exists!")

        data.update(tandem.toDict())
        with open(DEFAULT_FILEPATH, "w") as data_file:
            json.dump(data, data_file, indent=4)
    finally:
        load_tandems(window)


def set_tandem(window: MainWindow, index: int = None) -> None:
    if index is None:
        index = window.ui.listWidget_savedTandems.currentRow()

    if index < 0:
        return None

    tandems = list(window.tandems)
    if len(tandems) <= index:
        return None

    # using an index to select the dictionary to use
    selection = window.tandems[tandems[index]]

    # building the Tandem Model
    tandem = Tandem()
    tandem.fromDict(selection)

    window.tandem = tandem
    update_tandem_settings(window, tandem)
    load_tandem_models(window, tandem)

    # offsets
    window.tandem.setOffsets(height=window.tandem_height_offset, rotation=window.tandem_rotation_offset)
    tandemDisplay.update(window)


def load_tandem_models(window: MainWindow, tandem: Tandem) -> None:
    if tandem is None:
        return

    if not os.path.exists(tandem.shape_filepath):
        print(f"Tandem {tandem.name} display model is referencing an invalid filepath: {tandem.shape_filepath}")
        return

    tandem._base_shape = imports.get_file_shape(tandem.shape_filepath)

    tandemDisplay.update(window)


def applyOffsets(window: MainWindow, height_offset: float = None, rotation: float = None) -> None:
    print("tandem functions: applying offsets")
    if window.brachyCylinder is not None:
        tandem_height = -1 * window.brachyCylinder.diameter

    if height_offset is not None:
        window.tandem_height_offset = tandem_height + height_offset
    if rotation is not None:
        window.tandem_rotation_offset = rotation

    
    if window.tandem is not None:
        window.tandem.setOffsets(window.tandem_height_offset, window.tandem_rotation_offset)


def load_tandem_model(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Select Tandem Tool Model', window.import_default_folder,
                                           "Supported files (*.stl *.3mf *.obj *.stp *.step)")[0]
    if len(filename) == 0:
        return

    window.ui.tandem_lineEdit_toolModel.setText(filename)


def clear_tandem_settings(window: MainWindow) -> None:
    window.ui.tandem_lineEdit_toolModel.setText("")
    window.ui.lineEdit_tandemName.setText("")
    window.ui.btn_tandem_add_update.setObjectName("Add")
    window.ui.listWidget_savedTandems.clearSelection()
    window.tandem = None

    tandemDisplay.update(window)


def update_tandem_settings(window: MainWindow, tandem: Tandem) -> None:
    if tandem is None:
        clear_tandem_settings(window)
        return

    window.ui.tandem_lineEdit_toolModel.setText(tandem.shape_filepath)
    window.ui.lineEdit_tandemName.setText(tandem.name)
    window.ui.btn_tandem_add_update.setObjectName("Update")


def create_tandem(window: MainWindow):
    print("tandem functions: creating tandem")
    tandem = Tandem()
    tandem.channel_diameter = float(window.ui.tandem_spinbox_channel_diameter.value())
    tandem.tip_diameter = float(window.ui.tandem_spinbox_tip_diameter.value())   
    tandem.tip_angle = float(window.ui.tandem_spinbox_tip_angle.value()) 
    tandem.tip_thickness = float(window.ui.tandem_spinbox_tip_thickness.value()) 

    tandem.setOffsets(window.tandem_height_offset, window.tandem_rotation_offset)

    window.tandem = tandem
    tandemDisplay.update(window)