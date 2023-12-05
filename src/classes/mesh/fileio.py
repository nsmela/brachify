from pathlib import Path

from OCC.Extend.DataExchange import read_step_file, read_stl_file
from OCC.Extend.DataExchange import write_step_file, write_stl_file
from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Extend.DataExchange import write_stl_file
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone


def read_3d_file(filename: str, *args, **kwargs):
    """import a model file and generate a shape for it"""
    filepath = Path(filename)

    # make sure the path exists otherwise OCE get confused
    if not filepath.exists():
        raise FileNotFoundError(f"file does not exist: {filepath}")

    file_type = filepath.suffix.lower()

    if file_type != ".stl" and file_type != ".step" and file_type != ".stp":
        raise AssertionError(f"cannot read files of type {file_type} need to be .stl, .step or .stp")
    
    try:
        if file_type == ".stl":
            return read_stl_file(filepath._str)
        else:
            return read_step_file(filepath._str)
    except AssertionError as error_message:
        raise AssertionError(error_message)
    

def write_3d_file(filename: str, shape, *args, **kwargs):
    filepath = Path(filename)

    # make sure the path exists otherwise OCE get confused
    if not filepath.parent.exists():
        raise FileNotFoundError(f"folder does not exist: {filepath.parent}")

    file_type = filepath.suffix.lower()

    if file_type != ".stl" and file_type != ".step" and file_type != ".stp":
        raise AssertionError(
            f"cannot write files of type {file_type} need to be .stl, .step or .stp")

    file = filepath.__str__()  # needed or else the write unctions wont work well

    try:
        if file_type == ".step" or file_type == ".stp":
            write_step_file(filename= file, a_shape= shape, application_protocol= "AP203")
        else:
            write_stl_file(
                a_shape=shape,
                filename=file,
                mode="binary",
                linear_deflection=0.5,
                angular_deflection=0.3)
    except Exception as error_message:
        from src.classes.logger import log
        log.error(f"Unable to export {shape} to {filepath}\nError: {error_message}")
        raise AssertionError(error_message)
    
