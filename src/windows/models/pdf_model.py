from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image

import numpy as np
import subprocess
from datetime import datetime
import matplotlib.pyplot as plt

def export_pdf(window: MainWindow) -> None:

    def generate_cyl_pts(base, tip, radius, spacing, CylLen=160):
         # Example usage:
         # base = np.array([0,0,0])
         # tip = np.array([0,0,160])
         # radius = 15
          # spacing = 0.1
         # linepoints = np.array([[0,1,125],[0,0,127]]) #example start and endpoint for the first (needle tip) needle segment
         # cylinder_points, normals = generate_cyl_pts(base,tip,radius,spacing,CylLen=160)

         vec = np.array(tip-base)
          vec_normalized = vec / \
              np.sqrt(vec[0] ** 2 + vec[1] ** 2 + vec[2] ** 2)
           len_straight = CylLen-radius
            NumStepsStraight = int(np.ceil(len_straight / spacing))
            end_straight_section = base + vec_normalized * len_straight
            CenterLineStraight = np.linspace(
                base, end_straight_section, NumStepsStraight, endpoint=False)
            num_thetas = int(np.ceil(2*np.pi*radius/spacing))
            thetas = np.linspace(0, 2*np.pi, num_thetas, endpoint=False)

            # Step 2: Generate the Straight Part of the Cylinder
            CylinderRing = np.ones((num_thetas, 3))
            CylinderRing[:, 0] = CylinderRing[:, 0] * radius * np.sin(thetas)
            CylinderRing[:, 1] = CylinderRing[:, 1] * radius * np.cos(thetas)
            CylinderStraight = np.ones((NumStepsStraight, num_thetas, 3))
            CylinderStraight[:] = CylinderRing
            CylinderStraight[:, :, 2] = CylinderStraight[:,
                :, 2]*CenterLineStraight[:, 2, np.newaxis]

            # Step 3: Generate the Dome
            num_phis = int(np.ceil(np.pi/2*radius/spacing))
            phis = np.linspace(0, np.pi/2, num_phis)
            dome_radii = np.cos(phis)*radius

            dome_pts = np.ones((num_phis, num_thetas, 3))
            dome_pts[:, :, 0] = dome_pts[:, :, 0] * \
                np.sin(thetas) * dome_radii[:, np.newaxis]
            dome_pts[:, :, 1] = dome_pts[:, :, 1] * \
                np.cos(thetas) * dome_radii[:, np.newaxis]
            dome_pts[:, :, 2] = dome_pts[:, :, 2] * \
                np.sin(phis)[:, np.newaxis] * radius + len_straight

            # Step 4: Generate the Straight Part Normals
            vec_ring = CylinderRing - base
            # give each of the z component normals a bit of positive slope.
            vec_ring[:, 2] = 0.5
            vec_ring = vec_ring / \
                np.sqrt(np.einsum("ij,ij->i", vec_ring, vec_ring)
                        )[:, np.newaxis]
            vecs = np.ones((NumStepsStraight, num_thetas, 3))
            vecs[:] = vec_ring

            # Step 5: Generate the Dome Normals
            dome_base = end_straight_section
            dome_vecs = dome_pts - dome_base
            dome_vecs_reshaped = np.reshape(
                dome_vecs, (num_phis*num_thetas, 3))
            dome_disps_reshaped_normalized = dome_vecs_reshaped / \
                np.sqrt(np.einsum("ij,ij->i", dome_vecs_reshaped,
                        dome_vecs_reshaped))[:, np.newaxis]
            dome_vecs = np.reshape(
                dome_disps_reshaped_normalized, (num_phis, num_thetas, 3))

            cylinder_points = np.append(CylinderStraight, dome_pts)
            cylinder_points = np.reshape(
                cylinder_points, (NumStepsStraight*num_thetas+num_phis*num_thetas, 3))

            # Fix 1: the way this is made ends up adding a bunch of points (an amount of num_thetas) and vecs right at the tip of the dome. in this fix here we remove them.
            cylinder_points = cylinder_points[0:-num_thetas + 1]

            return cylinder_points

    def get_surface_intersection(surface_cloud, line_points, tol_mm=0.25):
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
        closest_points_on_line = line_points[0] + \
            projection_onto_line[:, np.newaxis] * line_direction

        # Check if the closest points are within the bounds of the line segment
        within_line_segment_bounds = np.logical_and(
            0 <= projection_onto_line, projection_onto_line <= np.linalg.norm(line_displacement))

        # Filter out points that are not within the line segment bounds
        closest_points_on_line = closest_points_on_line[within_line_segment_bounds]

        if len(closest_points_on_line) == 0:
            # If no points are within the line segment bounds, return None
            return None

        # Calculate the distance between each point in the cloud and its closest point on the line
        distances = np.linalg.norm(
            surface_cloud[within_line_segment_bounds] - closest_points_on_line, axis=1)

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
          needle_interstitial_lengths = []

           for needle in needles:
                needle = np.array(needle)
                first_line_segment = np.vstack([needle[1], needle[0]])
                length = get_interstitial_length(
                    cylinder_cloud, first_line_segment)

                if length is not None:
                    needle_interstitial_lengths.append(length)
                else:
                    needle_interstitial_lengths.append("Error")

            return needle_interstitial_lengths

    def extract_points_from_channels(channels):
        all_points = []

        for channel in channels:
            channel_points = []

            for point in channel.points:
                channel_points.append(point)

            all_points.append(channel_points)

        return all_points

    def process_lengths_and_create_data(is_lengths, protrusion_lengths):
        needle_data = []

        for idx, (length_mm, protrusion_length) in enumerate(zip(is_lengths, protrusion_lengths), start=1):
            # Convert lengths from mm to cm and round to one decimal place
            length_cm = round(length_mm / 10, 1)
            protrusion_length_cm = round(protrusion_length / 10, 1)

            # Create a tuple for needle_data with protrusion length in the third column
            needle_info = (
                f"Needle {idx}", f"{length_cm} cm", f"{protrusion_length_cm} cm")
            needle_data.append(needle_info)

        return needle_data

    def get_last_xy_points(needles):
        last_xy_points = []

        for needle in needles:
            # Check if the needle list is not empty and has at least 2 coordinates
            if needle and len(needle[-1]) >= 2:
                # Take only the first two coordinates (x and y)
                last_point = needle[-1][:2]
                last_xy_points.append(last_point)

        return last_xy_points

    def save_points_diagram(points, circle_radius, output_filepath, has_tandem=False):
        # Create a figure and axis
        fig, ax = plt.subplots()

        # Set axis limits to fit points inside a square with a border
        # Add a buffer of 1 to the radius
        square_size = 2 * (circle_radius + 1)
        ax.set_xlim(-square_size / 2, square_size / 2)
        ax.set_ylim(-square_size / 2, square_size / 2)

        # Plot the circle
        circle = plt.Circle((0, 0), circle_radius, color='black', fill=False)
        ax.add_artist(circle)

        # Plot each point as a circle with a number inside
        for i, (x, y) in enumerate(points, start=1):
            ax.add_artist(plt.Circle((x, y), 1.25, color='black', fill=False))
            if (i == 1 and has_tandem):
                ax.text(x, y, 'T', color='black', ha='center', va='center')
            else:
                ax.text(x, y, str(i), color='black', ha='center', va='center')

        # Add a filled black rectangle at the top center of the big circle
        tick_width = 0.2
        tick_height = 1.0
        tick_color = 'black'
        tick_vert_offset = 0.5
        if not has_tandem:
            rect = plt.Rectangle((-tick_width / 2, circle_radius - tick_vert_offset -
                                 tick_height), tick_width, tick_height, color=tick_color, fill=True)
            ax.add_artist(rect)

        # Remove axis markers and numbering
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_xticklabels([])
        ax.set_yticklabels([])

        # Set axis aspect ratio to be equal
        ax.set_aspect('equal', adjustable='box')

        # Save the plot as a PNG file
        plt.savefig(output_filepath, format='png', bbox_inches='tight')
        plt.close()

    def calculate_cumulative_lengths(needles):
        cumulative_lengths = []

        for needle in needles:
            cumulative_length = 0

            for i in range(1, len(needle)):
                x1, y1, z1 = map(float, needle[i - 1])
                x2, y2, z2 = map(float, needle[i])
                segment_length = ((x2 - x1)**2 + (y2 - y1)
                                  ** 2 + (z2 - z1)**2)**0.5
                cumulative_length += segment_length

            cumulative_lengths.append(cumulative_length)

        return cumulative_lengths

    def calculate_protrusion_lengths(needles, needle_length):
        cumulative_lengths = calculate_cumulative_lengths(needles)
        protrusion_lengths = [needle_length -
                              length for length in cumulative_lengths]
        return protrusion_lengths

    # Ask the user where to save the pdf and what to name it.
    filename = QFileDialog.getSaveFileName(
        window, 'Save solid as PDF', '', "PDF files (*.pdf)")[0]
    if len(filename) == 0:
        return

    # set the directory where to output the pdf
    pdf_output_dir = os.path.abspath(os.path.dirname(filename))
    filename = os.path.basename(filename)
    file_name_path = os.path.join(pdf_output_dir, filename)

    # make sure the path exists otherwise OCE gets confused
    if not os.path.isdir(pdf_output_dir):
        raise AssertionError(f"wrong path provided: {pdf_output_dir}")

    # get the relevent info for the pdf

    # get the needle centerline points from the window object
    needles = extract_points_from_channels(window.needles.channels)

    # generate the interstitial needle lengths
    base = np.array([0, 0, 0])
    tip = np.array([0, 0, 160])
    radius = window.brachyCylinder.diameter/2
    length = window.brachyCylinder.length

    is_lengths = get_all_interstitial_lengths(
        needles, base, tip, radius, 0.1, length)

    # generate the protrusion lengths
    needle_length = 160  # TODO expose this in the exports tab as an option.
    protrusion_lengths = calculate_protrusion_lengths(needles, needle_length)

    # get basepoints
    basepoints = get_last_xy_points(needles)
    fn = 'basemap.png'
    png_name_path = os.path.join(pdf_output_dir, fn)
    save_points_diagram(basepoints, radius, png_name_path)

    # get the patient name and ID
     #TODO: should actually be shown in the window somewhere
    # get the plan name and ID
     #TODO: should actually be shown in the window somewhere
    # Get today's date in the format "Month Day, Year"
     #TODO: should actually be shown in the window somewhere

    # Get today's date in the format "Month Day, Year"
    today_date = datetime.today().strftime('%B %d, %Y')

    # Header information
    header_info = "Patient Specific Cylindrical Template Reference Sheet"
    patient_name = window.PatientName
    patient_id = window.PatientID
    plan_label = window.plan_label

    # Create a PDF document
    pdf = SimpleDocTemplate(file_name_path, pagesize=letter)

    # Content elements for the PDF
    content = []

    # Add header information
    header_style = ParagraphStyle(
        'Header1',
        parent=getSampleStyleSheet()['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=13,  # Hardcoded font size in points
        alignment=1,  # 0=Left, 1=Center, 2=Right
    )

    header_text = "<u>{}</u>".format(header_info)
    content.append(Paragraph(header_text, header_style))

    # Center alignment for the following paragraphs
    centered_style = getSampleStyleSheet()['Normal']
    centered_style.alignment = 1  # 0=Left, 1=Center, 2=Right

    left_style = getSampleStyleSheet()['Normal']
    left_style.alignment = 0  # 0=Left, 1=Center, 2=Right

    content.append(Paragraph(f"Date: {today_date}", left_style))
    content.append(Paragraph(f"Patient Name: {patient_name}", left_style))
    content.append(Paragraph(f"Patient ID: {patient_id}", left_style))
    content.append(
        Paragraph(f"Plan Label: {plan_label} <br/> <br/>", left_style))
    content.append(Paragraph("<br/>", centered_style))

    # Add table with needle data
    # TODO: Add needle lable and channel number instead of "Needle 1" etc.
    length_label = "Protruding Length for " + str(needle_length) + "mm needle"
    data = [["Needle Number", "Interstitial Length", length_label]]
    for needle_number, interstitial_length, protruding_length in process_lengths_and_create_data(is_lengths, protrusion_lengths):
        data.append([needle_number, interstitial_length, protruding_length])

    table = Table(data)
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
    ])
    table.setStyle(table_style)
    content.append(table)

    # Add the image to the PDF
    # Adjust width and height as needed
    img = Image(png_name_path, width=300, height=300)
    content.append(img)

    # Build and save the PDF document
    pdf.build(content)

    # Open the generated PDF using the default PDF viewer
    try:
        if os.name == 'nt':  # Check if on Windows
            subprocess.Popen(['start', file_name_path], shell=True)
        elif os.name == 'posix':  # Check if on macOS/Linux
            subprocess.Popen(['open', file_name_path])
    except Exception as e:
        print(f"Unable to open the PDF: {e}")

    print('wait')
