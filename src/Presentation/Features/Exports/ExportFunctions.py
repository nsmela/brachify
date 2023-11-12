from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QListWidget, QMainWindow

from OCC.Core.TopoDS import TopoDS_Shape
from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
from OCC.Extend.DataExchange import write_stl_file
from OCC.Core.STEPControl import STEPControl_Writer, STEPControl_AsIs
from OCC.Core.Interface import Interface_Static_SetCVal
from OCC.Core.IFSelect import IFSelect_RetDone

from Presentation.MainWindow.core import MainWindow

import os


def generate_export(window: MainWindow) -> TopoDS_Shape:
    shape = TopoDS_Shape()

    try:
        # cylinder
        if window.brachyCylinder:
            shape = window.brachyCylinder.shape()
        else:
            return shape

    except Exception as error_message:
        print(error_message)

    try:
        # needles shown
        if window.needles:
            shape = BRepAlgoAPI_Cut(shape, window.needles.shape()).Shape()

    except Exception as error_message:
        print(error_message)

    try:
        # tandem
        if window.tandem:
            shape = BRepAlgoAPI_Cut(shape, window.tandem.shape()).Shape()

    except Exception as error_message:
        print(error_message)

    return shape


def export_stl(window:MainWindow) -> None:
    # ref: https://github.com/tpaviot/pythonocc-demos/blob/master/examples/core_export_stl.py
    filename = QFileDialog.getSaveFileName(window, 'Save solid as STL', '', "STL files (*.stl)")[0]
    if len(filename) == 0:
        return

    # set the directory where to output the
    stl_output_dir = os.path.abspath(os.path.dirname(filename))
    filename =  os.path.basename(filename)
    # make sure the path exists otherwise OCE get confused
    if not os.path.isdir(stl_output_dir):
        raise AssertionError(f"wrong path provided: {stl_output_dir}")

    # then we change the mesh resolution, and export as binary
    stl_high_resolution_file = os.path.join(stl_output_dir, filename)
    # we set the format to binary
    write_stl_file(
        window.display_export,
        stl_high_resolution_file,
        mode="binary",
        linear_deflection=0.5,
        angular_deflection=0.3,)


def export_step(window:MainWindow):
    # ref: https://github.com/tpaviot/pythonocc-demos/blob/master/examples/core_export_step_ap203.py
    filename = QFileDialog.getSaveFileName(window, 'Save solid as STEP', '', "STEP files (*.step)")[0]
    if len(filename) == 0:
        return
    
    # set the directory where to output the
    step_output_dir = os.path.abspath(os.path.dirname(filename))
    filepath = os.path.basename(filename)
    
    # make sure the path exists otherwise OCE get confused
    if not os.path.isdir(step_output_dir):
        raise AssertionError(f"wrong path provided: {step_output_dir}")

    output_filepath = os.path.join(step_output_dir, filepath)
    # initialize the STEP exporter
    step_writer = STEPControl_Writer()
    dd = step_writer.WS().TransferWriter().FinderProcess()
    print(dd)

    Interface_Static_SetCVal("write.step.schema", "AP203")

    # transfer shapes and write file
    shape = window.display_export
    step_writer.Transfer(shape, STEPControl_AsIs)
    status = step_writer.Write(output_filepath)

    if status != IFSelect_RetDone:
        raise AssertionError("load failed")


def generate_cyl_pts(base, tip, radius, spacing, CylLen=160):
        # Example usage:
        # base = np.array([0,0,0])
        # tip = np.array([0,0,160])
        # radius = 15
        # spacing = 0.1  
        # linepoints = np.array([[0,1,125],[0,0,127]]) #example start and endpoint for the first (needle tip) needle segment
        # cylinder_points, normals = generate_cyl_pts(base,tip,radius,spacing,CylLen=160)

        vec = np.array(tip-base)
        vec_normalized = vec / np.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
        len_straight = CylLen-radius
        NumStepsStraight = int(np.ceil(len_straight / spacing))
        end_straight_section = base + vec_normalized * len_straight
        CenterLineStraight = np.linspace(base, end_straight_section, NumStepsStraight, endpoint=False)
        num_thetas = int(np.ceil(2*np.pi*radius/spacing))
        thetas = np.linspace(0,2*np.pi,num_thetas,endpoint=False)

        # Step 2: Generate the Straight Part of the Cylinder
        CylinderRing = np.ones((num_thetas,3))
        CylinderRing[:, 0] = CylinderRing[:, 0] * radius * np.sin(thetas)
        CylinderRing[:, 1] = CylinderRing[:, 1] * radius * np.cos(thetas)
        CylinderStraight = np.ones((NumStepsStraight,num_thetas,3))
        CylinderStraight[:] = CylinderRing
        CylinderStraight[:,:,2] = CylinderStraight[:,:,2]*CenterLineStraight[:,2,np.newaxis]

        # Step 3: Generate the Dome
        num_phis = int(np.ceil(np.pi/2*radius/spacing))
        phis = np.linspace(0,np.pi/2,num_phis)
        dome_radii = np.cos(phis)*radius

        dome_pts = np.ones((num_phis,num_thetas,3))
        dome_pts[:,:,0] = dome_pts[:,:,0] * np.sin(thetas) * dome_radii[:,np.newaxis]
        dome_pts[:,:,1] = dome_pts[:,:,1] * np.cos(thetas) * dome_radii[:,np.newaxis]
        dome_pts[:,:,2] = dome_pts[:,:,2]* np.sin(phis)[:,np.newaxis] * radius + len_straight

        # Step 4: Generate the Straight Part Normals
        vec_ring = CylinderRing - base
        vec_ring[:,2] = 0.5 # give each of the z component normals a bit of positive slope.
        vec_ring = vec_ring / np.sqrt(np.einsum("ij,ij->i",vec_ring, vec_ring))[:,np.newaxis]
        vecs = np.ones((NumStepsStraight,num_thetas,3))
        vecs[:] = vec_ring

        # Step 5: Generate the Dome Normals
        dome_base = end_straight_section
        dome_vecs = dome_pts - dome_base
        dome_vecs_reshaped = np.reshape(dome_vecs, (num_phis*num_thetas,3))
        dome_disps_reshaped_normalized = dome_vecs_reshaped / np.sqrt(np.einsum("ij,ij->i",dome_vecs_reshaped, dome_vecs_reshaped))[:,np.newaxis]
        dome_vecs = np.reshape(dome_disps_reshaped_normalized,(num_phis,num_thetas,3) )

        cylinder_points = np.append(CylinderStraight,dome_pts)
        cylinder_points = np.reshape(cylinder_points,(NumStepsStraight*num_thetas+num_phis*num_thetas,3))

        # Fix 1: the way this is made ends up adding a bunch of points (an amount of num_thetas) and vecs right at the tip of the dome. in this fix here we remove them.
        cylinder_points = cylinder_points[0:-num_thetas + 1]

        return cylinder_points

def get_surface_intersection(surface_cloud, line_points, tol_mm = 0.25):
    # Convert the input lists to numpy arrays for efficient calculations
    surface_cloud = np.array(surface_cloud)
    line_points = np.array(line_points)

    # Check if the input arrays have the correct shapes
    if surface_cloud.shape[1] != 3 or line_points.shape[1] != 3:
        raise ValueError("Input arrays must have shape (n, 3)")

    # Calculate the direction vector of the line
    line_displacement = line_points[1] - line_points[0]
    line_displacement = line_displacement.astype(float)
    line_direction = line_displacement/np.linalg.norm(line_displacement)

    # Calculate the vector from one point on the line to each point in the point cloud
    vector_to_points = surface_cloud - line_points[0]

    # Project the vectors onto the line direction
    projection_onto_line = np.dot(vector_to_points, line_direction)

    # Calculate the closest points on the line to each point in the cloud
    closest_points_on_line = line_points[0] + projection_onto_line[:, np.newaxis] * line_direction

    # Check if the closest points are within the bounds of the line segment
    within_line_segment_bounds = np.logical_and(0 <= projection_onto_line, projection_onto_line <= np.linalg.norm(line_displacement))

    # Filter out points that are not within the line segment bounds
    closest_points_on_line = closest_points_on_line[within_line_segment_bounds]

    if len(closest_points_on_line) == 0:
        # If no points are within the line segment bounds, return None
        return None

    # Calculate the distance between each point in the cloud and its closest point on the line
    distances = np.linalg.norm(surface_cloud[within_line_segment_bounds] - closest_points_on_line, axis=1)

    if np.min(distances) > tol_mm:
         return None

    # Find the index of the point with the minimum distance
    min_distance_index = np.argmin(distances)
    

    # Return the point on the line and the corresponding point on the surface cloud
    return closest_points_on_line[min_distance_index], surface_cloud[within_line_segment_bounds][min_distance_index]

def get_interstitial_length(cylinder_points, linepoints):
    # Example Usage
    # length = get_interstitial_length(cylinder_points, linepoints)

    # Get the result from get_surface_intersection
    result = get_surface_intersection(cylinder_points, linepoints)
    if result != None:
        # Calculate the interstitial length based on the intersection point of the line segment with the surface.
        exit_point = result[0]
        end_point = linepoints[1]
        disp = end_point - exit_point
        length = np.linalg.norm(disp)
    else:
         length = 0
    return length

def get_all_interstitial_lengths(needles, base, tip, radius, spacing, CylLen=160):
        # Example usage:
        # needle_interstital_lengths = get_all_interstitial_lengths(needles, base, tip, radius, spacing, CylLen=160)
        # Where needles is a list of lists of needle coordinates.

        cylinder_cloud = generate_cyl_pts(base, tip, radius, spacing, CylLen)
        needle_interstital_lengths = []

        for needle in needles:
            first_line_segment = np.array(needle[-2], needle[-1])
            length = get_interstitial_length(cylinder_cloud, first_line_segment)
            
            if length is not None:
                needle_interstitial_lengths.append(length)
            else:
                needle_interstitial_lengths.append("Error")

        return needle_interstital_lengths