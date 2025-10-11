# Python script to estimate the parametric equations for a logarithmic spiral joining two arbitrary points


# section to import various standard libraries

import matplotlib.pyplot as plt     # import graphing library
import numpy as np                  # importing commonly used mathematical functions
from numpy import sqrt              # import various functions from numpy library
from class_line import *            # Import the line class


# ----- Additional Plotting Functions -------------------------------------------------------------------------------- #


def plot_xy_coordinates(x, y, style, label):
    """Plots a set of coordinates"""
    plt.plot(x, y, style, label=label)


def plot_graph_elements():
    """The basis for a general line plot"""
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axhline(0, color='black')   # x = 0
    plt.axvline(0, color='black')   # y = 0
    plt.grid()
    plt.show()


# ----- General Geometry Functions ----------------------------------------------------------------------------------- #

def calculate_points_from_chord(chord: float, stretch:float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Calculates the start and end coordinates of a spiral from the chord and the stretch"""
    a_x = sqrt(chord ** 2 / (stretch ** 2 + 1))
    b_y = stretch * a_x
    a, b = (a_x, 0), (0, b_y)
    return a, b


# ----- Diffuser Related Functions ----------------------------------------------------------------------------------- #

def diffuser_spiral_coordinates(inlet_width:float, outlet_width:float, stretch_centre:float, chord:float):
    """Calculates the start and end coordinates of the three spirals defining a diffuser"""
    chord_c1 = 1 + 1 / stretch_centre ** 2                               # 1st chord coefficient
    chord_c2 = outlet_width + inlet_width / stretch_centre               # 2nd chord coefficient
    chord_c3 = (inlet_width ** 2 + outlet_width ** 2) / 4 - chord ** 2   # 3rd chord coefficient
    b_y_centre = (sqrt(chord_c2 ** 2 - 4 * chord_c1 * chord_c3) - chord_c2) / (2 * chord_c1)
    b_y_inner = b_y_centre - outlet_width / 2
    b_y_outer = b_y_centre + outlet_width / 2
    a_x_centre = b_y_centre / stretch_centre
    a_x_inner = a_x_centre - inlet_width / 2
    a_x_outer = a_x_centre + inlet_width / 2
    stretch_inner = b_y_inner / a_x_inner
    stretch_outer = b_y_outer / a_x_outer
    b_inner, b_centre, b_outer = (0, b_y_inner), (0, b_y_centre), (0, b_y_outer)
    a_inner, a_centre, a_outer = (a_x_inner, 0), (a_x_centre, 0), (a_x_outer, 0)
    print("\nstretch of inner, centre, and outer curves respectively:")
    print(stretch_inner, stretch_centre, stretch_outer)
    spiral_coordinates = [["inner spiral", a_inner, b_inner],
                          ["centre spiral", a_centre, b_centre],
                          ["outer spiral", a_outer, b_outer]]
    return spiral_coordinates


# ----- Logarithmic Vane Related Functions --------------------------------------------------------------------------- #

def calculate_vane_spiral_end_points(thickness, chord_lower, stretch_lower, horizontal_pitch, vertical_pitch, ac_rad, bc_rad):

    # Calculate the start and end coordinates for the lower vane surface
    lower_width = chord_lower / np.sqrt(stretch_lower**2 +1)
    lower_height = stretch_lower * lower_width
    a_lower = Coordinate(name='a_lower', x=lower_width, y=0)
    b_lower = Coordinate(name='b_lower', x=0, y=lower_height)

    # Calculate the start coordinate for the upper vane surface
    a_x_upper = a_lower.x + abs(thickness * np.sin(ac_rad)) + vertical_pitch * np.cos(ac_rad)
    a_y_upper = a_lower.y + vertical_pitch
    a_upper = Coordinate(name='a_upper', x=a_x_upper, y=a_y_upper)

    # Calculate the end coordinate for the upper vane surface
    b_x_upper = b_lower.x + horizontal_pitch
    b_y_upper = b_lower.y + abs(thickness * np.cos(bc_rad)) - horizontal_pitch * np.sin(bc_rad)
    b_upper = Coordinate(name='b_upper', x=b_x_upper, y=b_y_upper)

    # Define lower and upper spiral_lines
    spiral_ends_lower = LineCoordinates('spiral_lower', a_lower, b_lower, LineType.SPIRAL)
    spiral_ends_upper = LineCoordinates('spiral_upper', a_upper, b_upper, LineType.SPIRAL)

    return spiral_ends_lower, spiral_ends_upper


def calculate_line_extensions_end_points(
        spiral_lower_ends:LineCoordinates,
        spiral_upper_ends:LineCoordinates,
        ac_rad:float,
        bc_rad:float,
        thickness:float):

    # Calculate the start and end coordinates for the upper vane extensions
    ext_start_x = spiral_lower_ends.start.x + thickness * np.sin(ac_rad)
    ext_start_y = spiral_lower_ends.start.y - thickness * np.cos(ac_rad)
    ext_end_x = spiral_lower_ends.end.x + thickness * np.sin(bc_rad)
    ext_end_y = spiral_lower_ends.end.y - thickness * np.cos(bc_rad)

    # bundle the coordinate components into the standard format
    ext_a_xy_1 = Coordinate('ext_a_xy_1', ext_start_x, ext_start_y)
    ext_a_xy_2 = Coordinate('ext_a_xy_2', spiral_upper_ends.start.x, spiral_upper_ends.start.y)
    ext_b_xy_1 = Coordinate('ext_b_xy_1', ext_end_x, ext_end_y)
    ext_b_xy_2 = Coordinate('ext_b_xy_2', spiral_upper_ends.end.x, spiral_upper_ends.end.y)

    # bundle the coordinates into the standard line format
    extension_ends_a = LineCoordinates('extension_line_a', ext_a_xy_1, ext_a_xy_2, LineType.LINE)
    extension_ends_b = LineCoordinates('extension_line_b', ext_b_xy_1, ext_b_xy_2, LineType.LINE)

    return extension_ends_a, extension_ends_b


def log_vane_coordinates(
        horizontal_pitch:float,
        vertical_pitch:float,
        thickness:float,
        stretch_lower:float,
        chord_lower:float,
        ac_deg:float,
        bc_deg:float):
    """Calculates the start and end coordinates of the three spirals defining a diffuser"""

    # Convert the angles to radians
    ac_rad = np.radians(ac_deg)
    bc_rad = np.radians(bc_deg)

    # Calculate the start and end coordinates for the lower and upper vane spirals
    spiral_ends_lower, spiral_ends_upper = calculate_vane_spiral_end_points(
        thickness, chord_lower, stretch_lower, horizontal_pitch, vertical_pitch, ac_rad, bc_rad)

    # Calculate the start and end coordinates for the line extensions
    extension_ends_a, extension_ends_b = calculate_line_extensions_end_points(
        spiral_ends_lower, spiral_ends_upper, ac_rad, bc_rad,thickness)

    # Calculate the start and end coordinates for the end fillet
    chamfer_a = LineCoordinates('chamfer_start_a', extension_ends_a.start, spiral_ends_lower.start, LineType.SEMICIRCLE)
    chamfer_b = LineCoordinates('chamfer_start_a', spiral_ends_lower.end, extension_ends_b.end, LineType.SEMICIRCLE)

    # Bundle the line and spiral coordinates into lists
    spiral_ends = [spiral_ends_lower, spiral_ends_upper]
    extension_ends = [extension_ends_a, extension_ends_b]
    fillet_ends = [chamfer_a, chamfer_b]

    return spiral_ends, extension_ends, fillet_ends