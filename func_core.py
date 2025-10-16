from typing import Any

from func_helper import *
from class_logarithmic_spiral import LogarithmicSpiral
from class_poly_line import PolyLine
from class_logarithmic_vane import LogarithmicVane
from copy import deepcopy
import numpy as np


def generate_log_spiral_from_points(a_xy:tuple[float, float], b_xy:tuple[float, float], ac_deg:float, bc_deg:float):
    """Fits a logarithmic spiral to a start and end point at a given start and end angle"""


    chord_line_spiral = Line
    s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg)

    # Create and plot the coordinates for the logarithmic spiral
    s_xx, s_yy = s.generate_spiral_coordinates()
    plot_xy_coordinates(x=s_xx, y=s_yy, style='-', label='connector')

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
        chord:float,
        stretch:float,
        thickness: float,
        ac_deg:float,
        bc_deg:float,
        show_plot=False) -> LogarithmicVane:
    """Creates the geometry of a curved diffuser from logarithmic spirals"""
    print('\nGenerating an expansion vane from logarithmic spirals')

    # Instantiate a vane instance from the input parameters
    vane = LogarithmicVane(
        horizontal_pitch=horizontal_pitch,
        vertical_pitch=vertical_pitch,
        chord_lower=chord,
        stretch_lower=stretch,
        thickness=thickness,
        ac_deg=ac_deg,
        bc_deg=bc_deg)

    # Plot the generated vane
    if show_plot:
        vane.plot_components()
        vane.plot()

    return vane


def  generate_vane_cascade(
        horizontal_pitch:float,
        vertical_pitch:float,
        chord:float,
        stretch:float,
        thickness: float,
        ac_deg:float,
        bc_deg:float,
        upstream_channel_length:float,
        downstream_channel_length:float,
        num_vanes=2,
        file_directory=None,
        stl_height = 1,
        stl_scale=1,
        show_plot=False):

    """Generates a cascade of expansion vanes from a single logarithmic expansion vane"""
    print('\nGenerating a expansion vane cascade from a singe logarithmic vane')

    vane = generate_vane(horizontal_pitch, vertical_pitch, chord, stretch, thickness, ac_deg, bc_deg, show_plot)

    vane.generate_vane_cascade(
        upstream_channel_length, downstream_channel_length, num_vanes, file_directory, stl_height, stl_scale, show_plot)













