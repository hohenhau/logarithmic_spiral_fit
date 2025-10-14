from func_helper import *
from class_logarithmic_spiral import LogarithmicSpiral
from class_poly_line import PolyLine
from copy import deepcopy
import numpy as np


def generate_log_spiral_from_points(a_xy, b_xy, ac_deg, bc_deg):
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


def generate_log_spiral_from_chord(chord, stretch, ac_deg, bc_deg):
    """Fits a logarithmic spiral to a specific chord and stretch at a given start and end angle"""
    a_xy, b_xy = calculate_points_from_chord(chord, stretch)
    generate_log_spiral_from_points(a_xy, b_xy, ac_deg, bc_deg)


def generate_diffuser_from_geometry(inlet_width, outlet_width, stretch, chord, ac_deg, bc_deg):
    """Creates the geometry of a curved diffuser from logarithmic spirals"""
    coordinate_lines = diffuser_coordinates(inlet_width, outlet_width, stretch, chord)
    spirals = list()
    for line in coordinate_lines:
        a_xy = line.start.x, line.start.y
        b_xy = line.end.x, line.end.y
        s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg, line.name, line.style)
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


def generate_vane_from_geometry(horizontal_pitch, vertical_pitch, thickness, chord, stretch, ac_deg, bc_deg):
    """Creates the geometry of a curved diffuser from logarithmic spirals"""

    # Generate spiral and line end coordinates from geometry
    spiral_ends, extension_ends, fillet_ends = calculate_log_vane_component_coordinates(
        horizontal_pitch, vertical_pitch, thickness,stretch, chord, ac_deg, bc_deg)

    spirals = list()
    for points in spiral_ends:
        points_start = points.start.x, points.start.y
        points_end = points.end.x, points.end.y
        points.spiral = LogarithmicSpiral(points_start, points_end, ac_deg, bc_deg, points.name)
        points.spiral.calculate_origin_offsets(horizontal_pitch, vertical_pitch, thickness)

    # Save the spiral equations to the local directory
    LogarithmicSpiral.save_spiral_equations(spirals, "./equations.csv")

    # Set a clockwise order for the various components of the logarithmic vane
    order = [extension_ends[0], spiral_ends[0], extension_ends[1], fillet_ends[1], spiral_ends[1], fillet_ends[0]]
    vane_xx, vane_yy = list(), list()
    for line_coordinates in order:
        reverse = True if line_coordinates.name == 'spiral_lower' else False
        xx, yy = line_coordinates.generate(reverse=reverse)
        plot_xy_coordinates(xx, yy, line_coordinates.style, line_coordinates.name)
        # Add coordinates of component to combined coordinate list
        vane_xx.extend(xx[:-1])
        vane_yy.extend(yy[:-1])
    plot_graph_elements()

    # Add the first coordinate to the end, to close the geometry
    vane_xx.append(vane_xx[0])
    vane_yy.append(vane_yy[0])

    # Find the mid-points of the fillets for the cascade extension
    vane_ends = list()
    for line_coordinates in fillet_ends:
        name = line_coordinates.name
        fillet_a_xx, fillet_a_yy = line_coordinates.generate_spiral_coordinates()
        fillet_mid = Coordinate(fillet_a_xx[len(fillet_a_xx) // 2], fillet_a_yy[len(fillet_a_yy) // 2], name=name)
        vane_ends.append(fillet_mid)

    return vane_xx, vane_yy, vane_ends


def generate_vane_cascade_from_vane(horizontal_pitch, vertical_pitch, ac_deg, bc_deg, channel_length, vane, num_vanes=2):

    if num_vanes < 2:
        print('Minimum number of vanes must be at least 2. Setting number of vanes to 2')
        num_vanes = 2

    # Convert the start and end angles to degrees
    ac_rad, bc_rad = np.radians(ac_deg), np.radians(bc_deg)

    # Extract the various components from the vane tuple
    vane_xx, vane_yy, vane_ends = vane

    vanes = list()
    for i in range(num_vanes):
        vane_poly_line = PolyLine.generate_poly_line_from_list_of_floats(xx=vane_xx, yy=vane_yy, label='vane')
        offset_x = i * horizontal_pitch
        offset_y = i * vertical_pitch
        vane_poly_line.offset(x=offset_x, y=offset_y)
        vanes.append(vane_poly_line)
        vane_poly_line.plot()






    channels = list()
    for vane_end in vane_ends:
        location = vane_end.name.split('_')[-1]
        if location != 'a' and location != 'b':
            raise ValueError('channel location not recognised. Must be "a" or "b"')
        name = f'channel_{location}_inner'
        orientation = -1 if location == 'a' else 1
        angle = ac_rad if location == 'a' else bc_rad
        channel_start_x = vane_end.x + orientation * channel_length * np.cos(angle)
        channel_start_y = vane_end.y + orientation * channel_length * np.sin(angle)
        channel_start = Coordinate(channel_start_x, channel_start_y)
        channel = Line(start=channel_start, end=vane_end, name=name)
        channels.append(channel)

    # outer_channels = list()
    # for channel in channels:
    #     outer_channel_
    #     outer


    for channel in channels:
        channel_xx, channel_yy = channel.generate_spiral_coordinates()
        plot_xy_coordinates(x_or_points=channel_xx, y=channel_yy, label=channel.name)


    plot_graph_elements()















