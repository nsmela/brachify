from PyQt5.QtWidgets import QFileDialog

from OCC.Extend.ShapeFactory import translate_shp, rotate_shape
from OCC.Core.gp import gp, gp_Vec

from Presentation.MainWindow.core import MainWindow
import Presentation.Features.Imports.ImportFunctions as imports
import Presentation.Features.Tandem.TandemDisplay as tandemDisplay
import Application.BRep.Helper as brep
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
            window.tandems = json.load(data_file)
    except FileNotFoundError as error_message:
        print(f"File {data_filepath} was not found! \n {error_message}")

    if window.tandems is None:
        return

    for tandem in window.tandems:
        window.ui.listWidget_savedTandems.addItem(tandem)

    set_tandem(window)


def save_tandem(window: MainWindow) -> bool:
    """attempts to add or update the json file containing the tandem settings"""
    tandem_name = window.ui.lineEdit_tandemName.text()
    tandem_display_model = window.ui.tandem_lineEdit_displayModel.text()
    tandem_tool_model = window.ui.tandem_lineEdit_toolModel.text()
    index = window.ui.listWidget_savedTandems.currentRow()

    # check if info is enough to proceed
    if not tandem_name:
        return False
    if not tandem_display_model:
        return False
    if not tandem_tool_model:
        return False

    # turn info into dict for json
    tandem = TandemModel()
    tandem.name = tandem_name
    tandem.shape_filepath = os.path.join(tandem_dir,
                                         f"{tandem_name}_display{os.path.splitext(tandem_display_model)[1]}")
    tandem.tool_filepath = os.path.join(tandem_dir, f"{tandem_name}_tool{os.path.splitext(tandem_tool_model)[1]}")

    # check if file exists, if not create a blank one
    try:
        # load file if exists
        with open(data_filepath, "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        # if not, save the info instead
        # copy model files to the tandem directory
        result = shutil.copy(tandem_display_model, tandem.shape_filepath)
        print(f"display model copied to {result}")

        result = shutil.copy(tandem_tool_model, tandem.tool_filepath)
        print(f"tool model copied to {result}")

        data = tandem.toDict()
        with open(data_filepath, "x") as data_file:
            json.dump(data, data_file, indent=4)
    except Exception as error_message:
        print(f"Tandem save failed: {error_message}")
        return False
    else:
        # copy model files to the tandem directory
        try:
            result = shutil.copy(tandem_display_model, tandem.shape_filepath)
            print(f"display model copied to {result}")
        except shutil.SameFileError as error_message:
            print(f"File {tandem.shape_filepath} already exists!")

        try:
            result = shutil.copy(tandem_tool_model, tandem.tool_filepath)
            print(f"tool model copied to {result}")
        except shutil.SameFileError as error_message:
            print(f"File {tandem.tool_filepath} already exists!")

        data.update(tandem.toDict())
        with open(data_filepath, "w") as data_file:
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
    tandem = TandemModel()
    tandem.fromDict(selection)

    window.tandem = tandem
    update_tandem_settings(window, tandem)
    load_tandem_models(window, tandem)
    window.tandem = apply_tandem_offsets(tandem, position=window.tandem_offset_position,
                                         rotation=window.tandem_offset_rotation)
    tandemDisplay.update(window)


def load_tandem_models(window: MainWindow, tandem: TandemModel) -> None:
    if not tandem:
        return

    if not os.path.exists(tandem.shape_filepath):
        print(f"Tandem {tandem.name} display model is referencing an invalid filepath: {tandem.shape_filepath}")
        return

    if not os.path.exists(tandem.tool_filepath):
        print(f"Tandem {tandem.name} tool model is referencing an invalid filepath: {tandem.tool_filepath}")
        return

    tandem.shape = imports.get_file_shape(tandem.shape_filepath)
    tandem.tool_shape = imports.get_file_shape(tandem.tool_filepath)

    tandemDisplay.update(window)



def apply_tandem_offsets(tandem: TandemModel, position: list = [0.0, 0.0, 0.0], rotation: float = 0.0) -> TandemModel:
    if not tandem:
        return None

    offset = gp_Vec(0.0, 0.0, position[2] - 9.0)

    if tandem.shape:
        tandem.shape = rotate_shape(shape=tandem.shape, axis=gp.OZ(), angle=rotation)
        tandem.shape = translate_shp(tandem.shape, offset)

    if tandem.tool_shape:
        tandem.tool_shape = rotate_shape(shape=tandem.tool_shape, axis=gp.OZ(), angle=rotation)
        tandem.tool_shape = translate_shp(tandem.tool_shape, offset)

    tandem = extend(tandem)

    return tandem


def extend(tandem: TandemModel) -> TandemModel:
    try:
        tandem.shape = brep.extend_bottom_face(tandem.shape)
        tandem.tool_shape = brep.extend_bottom_face(tandem.tool_shape)
    except Exception as error_message:
        print(f"Lower face extension failed! {error_message}")

    return tandem


def load_tandem_display_model(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Select Tandem Display Model', '',
                                           "Supported files (*.stl *.3mf *.obj *.stp *.step)")[0]
    if len(filename) == 0:
        return

    window.ui.tandem_lineEdit_displayModel.setText(filename)


def load_tandem_tool_model(window: MainWindow) -> None:
    filename = QFileDialog.getOpenFileName(window, 'Select Tandem Tool Model', '',
                                           "Supported files (*.stl *.3mf *.obj *.stp *.step)")[0]
    if len(filename) == 0:
        return

    window.ui.tandem_lineEdit_toolModel.setText(filename)


def clear_tandem_settings(window: MainWindow) -> None:
    window.ui.tandem_lineEdit_displayModel.setText("")
    window.ui.tandem_lineEdit_toolModel.setText("")
    window.ui.lineEdit_tandemName.setText("")
    window.ui.btn_tandem_add_update.setObjectName("Add")
    window.ui.listWidget_savedTandems.clearSelection()
    window.tandem = None

    tandemDisplay.update(window)


def update_tandem_settings(window: MainWindow, tandem: TandemModel) -> None:
    if tandem is None:
        clear_tandem_settings(window)
        return

    window.ui.tandem_lineEdit_displayModel.setText(tandem.shape_filepath)
    window.ui.tandem_lineEdit_toolModel.setText(tandem.tool_filepath)
    window.ui.lineEdit_tandemName.setText(tandem.name)
    window.ui.btn_tandem_add_update.setObjectName("Update")
