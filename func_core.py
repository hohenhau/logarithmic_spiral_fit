from func_helper import *
from class_logarithmic_spiral import LogarithmicSpiral
from class_poly_line import PolyLine
from copy import deepcopy
import numpy as np


def generate_log_spiral_from_points(a_xy:tuple[float, float], b_xy:tuple[float, float], ac_deg:float, bc_deg:float):
    """Fits a logarithmic spiral to a start and end point at a given start and end angle"""


    chord_line_spiral = Line
    s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg)

    # Create and plot the coordinates for the logarithmic spiral
    s_xx, s_yy = s.generate_spiral_coordinates()
    plot_xy_coordinates(x_or_points=s_xx, y=s_yy, style='-', label='connector')

    # Define construction geometry
    connecting_line = [a_xy, b_xy]
    tangent_triangle = [a_xy, s.c_xy, b_xy]
    origin_triangle = [a_xy, s.origin_xy, b_xy]

    # Plot construction geometry
    plot_xy_coordinates(connecting_line, style='-o', label='connector')
    plot_xy_coordinates(tangent_triangle, style='-o', label='tangent')
    plot_xy_coordinates(origin_triangle, style='-o', label='origin')

    # Plot the general graph elements (title, axis, etc.) and print spiral equations
    plot_graph_elements()
    print(s)


def generate_log_spiral_from_chord(chord:float, stretch:float, ac_deg:float, bc_deg:float):
    """Fits a logarithmic spiral to a specific chord and stretch at a given start and end angle"""
    a_xy, b_xy = calculate_points_from_chord(chord, stretch)
    generate_log_spiral_from_points(a_xy, b_xy, ac_deg, bc_deg)


def generate_diffuser(inlet_width:float, outlet_width:float, chord:float, stretch:float, ac_deg:float, bc_deg:float):
    """Creates the geometry of a curved diffuser from logarithmic spirals"""
    coordinate_lines = diffuser_coordinates(inlet_width, outlet_width, stretch, chord)
    spirals = list()
    for line in coordinate_lines:
        a_xy = line.start.x, line.start.y
        b_xy = line.end.x, line.end.y
        s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg, line.label, line.style)
        s.calculate_origin_offsets(inlet_width, outlet_width)
        spirals.append(s)
    LogarithmicSpiral.tabulate_spirals(spirals)
    for s in spirals:
        print(s)
    for s in spirals:
        s_xx, s_yy = s.generate_spiral_coordinates()
        plot_xy_coordinates(s_xx, s_yy, s.style, s.name)
    plot_graph_elements()
    LogarithmicSpiral.save_spiral_equations(spirals, "./equations.csv")


def generate_vane(
        horizontal_pitch:float,
        vertical_pitch:float,
        thickness:float,
        chord:float,
        stretch:float,
        ac_deg:float,
        bc_deg:float) -> tuple[PolyLine, list[Coordinate]]:
    """Creates the geometry of a curved diffuser from logarithmic spirals"""
    print('\nGenerating an expansion vane from logarithmic spirals')

    # Convert degree angles to radians
    ac_rad = np.radians(ac_deg)
    bc_rad = np.radians(bc_deg)

    # Generate spiral and line end coordinates from geometry
    chord_lines = calculate_chord_lines(
        horizontal_pitch=horizontal_pitch,
        vertical_pitch=vertical_pitch,
        thickness=thickness,
        chord_lower=chord,
        stretch_lower=stretch,
        ac_rad=ac_rad,
        bc_rad=bc_rad)

    # Instantiate various components
    spirals = list()
    vane_ends = list()
    vane = PolyLine(label='vane')
    vane.xx, vane.yy = list(), list()

    # Loop over the chord lines to generate PolyLines and fill containers
    for chord_line in chord_lines:

        # Calculate the spiral geometry if the chord line represents a spiral
        if chord_line.line_type == LineType.SPIRAL:
            start_xy = chord_line.start.x, chord_line.start.y
            end_xy = chord_line.end.x, chord_line.end.y
            chord_line.spiral = LogarithmicSpiral(start_xy, end_xy, ac_deg, bc_deg, chord_line.label)
            chord_line.spiral.calculate_origin_offsets(horizontal_pitch, vertical_pitch, thickness)
            spirals.append(chord_line.spiral)

        # Reverse the coordinates if the chord line represents the lower spiral
        reverse = True if chord_line.label == 'spiral_lower' else False

        # Generate a PolyLine from the chord line
        poly_line = PolyLine.generate_from_line(chord_line, reverse=reverse, label=chord_line.label)

        # Add coordinates of component to combined coordinate list
        vane.xx.extend(poly_line.xx[:-1])
        vane.yy.extend(poly_line.yy[:-1])

        # Find the mod points of the semicircle to determine vane termination points
        if chord_line.line_type == LineType.SEMICIRCLE:
            mid_x, mid_y = poly_line.xx[len(poly_line.xx) // 2], poly_line.yy[len(poly_line.yy) // 2]
            fillet_mid = Coordinate(mid_x, mid_y, label=chord_line.label)
            vane_ends.append(fillet_mid)

        # Plot the current PolyLine
        poly_line.plot()

    # Plot additional graph elements (equal axis, etc.)
    plot_graph_elements()

    # Save the spiral equations to the local directory
    LogarithmicSpiral.save_spiral_equations(spirals, "./equations.csv")

    return vane, vane_ends


def generate_vane_cascade(
        horizontal_pitch:float,
        vertical_pitch:float,
        ac_deg:float,
        bc_deg:float,
        upstream_channel_length:float,
        downstream_channel_length:float,
        vane_poly_line_and_ends:tuple[PolyLine, list[Coordinate]],
        num_vanes=2,
        file_directory=None,
        stl_height = 1,
        stl_scale=1):

    """Generates a cascade of expansion vanes from a single logarithmic expansion vane"""
    print('\nGenerating a expansion vane cascade from a singe logarithmic vane')

    if num_vanes < 2:
        print('Minimum number of vanes must be at least 2. Setting number of vanes to 2')
        num_vanes = 2

    # Convert the start and end angles to degrees
    ac_rad, bc_rad = np.radians(ac_deg), np.radians(bc_deg)

    # Extract the various components from the vane tuple
    vane_poly_line, vane_ends_lower = vane_poly_line_and_ends

    vanes = list()
    for i in range(num_vanes):
        vane_poly_line_copy = deepcopy(vane_poly_line)
        offset_x = i * horizontal_pitch
        offset_y = i * vertical_pitch
        vane_poly_line_copy.offset(x=offset_x, y=offset_y)
        vanes.append(vane_poly_line_copy)
        vane_poly_line_copy.plot()
        vanes.append(vane_poly_line_copy)

    channel_walls = list()
    channel_ends = list()
    for vane_end_lower in vane_ends_lower:

        location = vane_end_lower.label.split('_')[-1]
        if location != 'a' and location != 'b':
            raise ValueError('channel location not recognised. Must be "a" or "b"')

        # Calculate the upper vane end
        num_gaps = num_vanes - 1
        vane_end_upper = deepcopy(vane_end_lower)
        vane_end_upper.offset(x=horizontal_pitch * num_gaps, y=vertical_pitch * num_gaps)

        if location == 'a' and location != 'b':
            orientation = -1
            extension_angle = ac_rad
            end_label = 'inlet'
            channel_length = upstream_channel_length
        else:
            orientation = 1
            extension_angle = bc_rad
            end_label = 'outlet'
            channel_length = downstream_channel_length

        # Calculate the lower channel point
        channel_start_x = vane_end_lower.x + orientation * channel_length * np.cos(extension_angle)
        channel_start_y = vane_end_lower.y + orientation * channel_length * np.sin(extension_angle)
        end_lower = Coordinate(channel_start_x, channel_start_y, label=f'channel_{location}_lower')

        # Calculate the upper channel point
        x_offset, y_offset = horizontal_pitch * num_gaps, vertical_pitch * num_gaps
        end_upper = deepcopy(end_lower)
        end_upper.offset(x_offset, y_offset)

        # Calculate the lower-mid and upper-mid channel points
        projected_angle = extension_angle - (np.pi / 2)
        pitch_angle = np.arctan(vertical_pitch / horizontal_pitch)
        offset_angle = projected_angle - pitch_angle
        diagonal_pitch = (horizontal_pitch ** 2 + vertical_pitch ** 2) ** 0.5
        projected_distance = np.cos(offset_angle) * (diagonal_pitch * num_gaps / 3)
        x_offset = projected_distance * np.cos(projected_angle)
        y_offset = projected_distance * np.sin(projected_angle)
        end_lower_mid = deepcopy(end_lower)
        end_lower_mid.offset(x_offset, y_offset)
        end_upper_mid = deepcopy(end_upper)
        end_upper_mid.offset(-x_offset, -y_offset)

        # Define coordinates in side walls and end wall
        lower_coordinates = [vane_end_lower, end_lower]
        upper_coordinates = [vane_end_upper, end_upper]
        end_coordinates = [end_lower, end_lower_mid, end_upper_mid, end_upper]

        # Generate PolyLines from the list of coordinates
        lower_poly_line = PolyLine.generate_from_coordinate_list(lower_coordinates, label=f'cyclic_{location}_01')
        upper_poly_line = PolyLine.generate_from_coordinate_list(upper_coordinates, label=f'cyclic_{location}_02')
        end_poly_line = PolyLine.generate_from_coordinate_list(end_coordinates, label=end_label)

        # Plot the various PolyLines
        lower_poly_line.plot()
        upper_poly_line.plot()
        end_poly_line.plot()

        # Group the channel walls and ends into the relevant list
        channel_ends.append(end_poly_line)
        channel_walls.append(lower_poly_line)
        channel_walls.append(upper_poly_line)

    plot_graph_elements()

    for channel_wall in channel_walls:
        PolyLine.create_stl_file_from_xy_poly_line(
            poly_lines=channel_wall,
        height=stl_height,
        file_directory=file_directory)

    for channel_end in channel_ends:
        PolyLine.create_stl_file_from_xy_poly_line(
            poly_lines=channel_end,
        height=stl_height,
        file_directory=file_directory)

    PolyLine.create_stl_file_from_xy_poly_line(
        poly_lines=vanes,
        height=stl_height,
        file_directory=file_directory)















