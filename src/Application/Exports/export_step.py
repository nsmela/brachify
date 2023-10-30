# https://dev.opencascade.org/doc/occt-6.9.1/overview/html/occt_user_guides__step.html#occt_step_3_4
# https://github.com/tpaviot/pythonocc-demos/blob/master/examples/core_export_step_ap203.py

from OCC.Extend.DataExchange import write_stl_file
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone

import os


def export_step(filepath: str, shape):
    # ref: https://github.com/tpaviot/pythonocc-demos/blob/master/examples/core_export_step_ap203.py

    # set the directory where to output the
    step_output_dir = os.path.abspath(os.path.dirname(filepath))
    filename = os.path.basename(filepath)
    # make sure the path exists otherwise OCE get confused
    if not os.path.isdir(step_output_dir):
        raise AssertionError(f"wrong path provided: {step_output_dir}")

    output_filepath = os.path.join(step_output_dir, filename)
    # initialize the STEP exporter
    step_writer = STEPControl_Writer()
    dd = step_writer.WS().TransferWriter().FinderProcess()
    print(dd)

    Interface_Static_SetCVal("write.step.schema", "AP203")

    # transfer shapes and write file
    step_writer.Transfer(shape, STEPControl_AsIs)
    status = step_writer.Write(output_filepath)

    if status != IFSelect_RetDone:
        raise AssertionError("load failed")