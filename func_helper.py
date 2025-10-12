# Python script to estimate the parametric equations for a logarithmic spiral joining two arbitrary points


# section to import various standard libraries

import matplotlib.pyplot as plt     # import graphing library
import numpy as np                  # importing commonly used mathematical functions
from numpy import sqrt              # import various functions from numpy library
from class_line import *            # Import the line class


# ----- Additional Plotting Functions -------------------------------------------------------------------------------- #


def plot_xy_coordinates(x_or_points, y=None, style='-', label=None):
    """
    Plot a set of X and Y coordinates

    Parameters
    ----------
    x_or_points : list[float] | list[tuple[float, float]]
        X values, or a list of (x, y) coordinate pairs.
    y : list[float], optional
        Y values if x_or_points is a list of X values.
    style : str, default '-'
        Line style passed to matplotlib.
    label : str, optional
        Label for the plot legend.
    """

    if y is None:  # Single list of (x, y)
        try:
            x, y = zip(*x_or_points)
        except (TypeError, ValueError):
            raise ValueError("If 'y' is not provided, 'x_or_points' must be a list of (x, y) pairs.")
    else:  # Separate x and y lists
        x = x_or_points
        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")
    plt.plot(x, y, style, label=label)


def plot_graph_elements():
    """The basis for a general line plot"""
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axhline(0, color='black')   # x = 0
    plt.axvline(0, color='black')   # y = 0
    plt.grid(True)
    plt.axis('equal')   # Ensures X and Y have the same scale
    plt.show()


# ----- General Geometry Functions ----------------------------------------------------------------------------------- #

def calculate_points_from_chord(chord: float, stretch:float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Calculates the start and end coordinates of a spiral from the chord and the stretch"""
    a_x = sqrt(chord ** 2 / (stretch ** 2 + 1))
    b_y = stretch * a_x
    a, b = (a_x, 0), (0, b_y)
    return a, b


def order_points(x: list[float], y: list[float], clockwise: bool = True):
    """
    Combine unordered x, y coordinates into an ordered curve.

    Parameters
    ----------
    x, y : list[float]
        Unordered coordinates (same length).
    clockwise : bool, optional
        If True, order points clockwise; if False, counterclockwise.

    Returns
    -------
    x_sorted, y_sorted : np.ndarray
        Ordered coordinate arrays.
    """

    # Combine into Nx2 array and remove duplicates
    points = np.unique(np.column_stack((x, y)), axis=0)

    # Compute centroid
    centroid = np.mean(points, axis=0)

    # Compute polar angles relative to centroid
    angles = np.arctan2(points[:, 1] - centroid[1], points[:, 0] - centroid[0])

    # Sort by angle
    sort_idx = np.argsort(angles)
    if clockwise:
        sort_idx = sort_idx[::-1]  # reverse order
    points_sorted = points[sort_idx]

    # Find index of point with smallest Y (tie-breaker: smallest X)
    start_idx = np.lexsort((points_sorted[:, 0], points_sorted[:, 1]))[0]

    # Rotate so the lowest-Y point is first
    points_sorted = np.roll(points_sorted, -start_idx, axis=0)

    return points_sorted[:, 0], points_sorted[:, 1]


# ----- Diffuser Related Functions ----------------------------------------------------------------------------------- #

def diffuser_coordinates(
        inlet_width:float,
        outlet_width:float,
        stretch_centre:float,
        chord:float) -> list[LineAttributes]:
    """Calculates the start and end coordinates of the three spirals defining a diffuser"""

    # Calculate the chord coefficients
    chord_c1 = 1 + 1 / stretch_centre ** 2                               # 1st chord coefficient
    chord_c2 = outlet_width + inlet_width / stretch_centre               # 2nd chord coefficient
    chord_c3 = (inlet_width ** 2 + outlet_width ** 2) / 4 - chord ** 2   # 3rd chord coefficient

    # Calculate the end points of the various spirals
    b_y_centre = (sqrt(chord_c2 ** 2 - 4 * chord_c1 * chord_c3) - chord_c2) / (2 * chord_c1)
    b_y_inner = b_y_centre - outlet_width / 2
    b_y_outer = b_y_centre + outlet_width / 2
    a_x_centre = b_y_centre / stretch_centre
    a_x_inner = a_x_centre - inlet_width / 2
    a_x_outer = a_x_centre + inlet_width / 2

    # Define coordinates for inner spiral
    a_inner = Coordinate(x=a_x_inner, y=0)
    b_inner = Coordinate(x=0, y=b_y_inner)
    ab_inner = LineAttributes(start=a_inner, end=b_inner, line_type=LineType.SPIRAL, name='inner')

    # Define coordinates for centre spiral
    a_centre = Coordinate(x=a_x_centre, y=0)
    b_centre = Coordinate(x=0, y=b_y_centre)
    ab_centre = LineAttributes(start=a_centre, end=b_centre, line_type=LineType.SPIRAL, name='centre', style='--')

    # Define coordinates for outer spiral
    a_outer = Coordinate(x=a_x_outer, y=0)
    b_outer = Coordinate(x=0, y=b_y_outer)
    ab_outer = LineAttributes(start=a_outer, end=b_outer, line_type=LineType.SPIRAL, name='outer')

    # Calculate and print the stretch of the spirals to the console
    stretch_inner = b_y_inner / a_x_inner
    stretch_outer = b_y_outer / a_x_outer
    print("\nstretch of inner, centre, and outer curves respectively:")
    print(stretch_inner, stretch_centre, stretch_outer)

    return [ab_inner, ab_centre, ab_outer]


# ----- Logarithmic Vane Related Functions --------------------------------------------------------------------------- #

def calculate_vane_spiral_end_points(thickness, chord_lower, stretch_lower, horizontal_pitch, vertical_pitch, ac_rad, bc_rad):

    # Calculate the start and end coordinates for the lower vane surface
    lower_width = chord_lower / np.sqrt(stretch_lower**2 +1)
    lower_height = stretch_lower * lower_width
    a_lower = Coordinate(x=lower_width, y=0)
    b_lower = Coordinate(x=0, y=lower_height)

    # Calculate the start coordinate for the upper vane surface
    a_x_upper = a_lower.x + abs(thickness * np.sin(ac_rad)) + vertical_pitch * np.cos(ac_rad)
    a_y_upper = a_lower.y + vertical_pitch
    a_upper = Coordinate(x=a_x_upper, y=a_y_upper)

    # Calculate the end coordinate for the upper vane surface
    b_x_upper = b_lower.x + horizontal_pitch
    b_y_upper = b_lower.y + abs(thickness * np.cos(bc_rad)) - horizontal_pitch * np.sin(bc_rad)
    b_upper = Coordinate(x=b_x_upper, y=b_y_upper)

    # Define lower and upper spiral_lines
    spiral_ends_lower = LineAttributes(start=a_lower, end=b_lower, line_type=LineType.SPIRAL, name='spiral_lower')
    spiral_ends_upper = LineAttributes(start=a_upper, end=b_upper, line_type=LineType.SPIRAL, name='spiral_upper')

    return spiral_ends_lower, spiral_ends_upper


def calculate_line_extensions_end_points(
        spiral_lower_ends:LineAttributes,
        spiral_upper_ends:LineAttributes,
        ac_rad:float,
        bc_rad:float,
        thickness:float):

    # Calculate the start and end coordinates for the upper vane extensions
    ext_start_x = spiral_lower_ends.start.x + thickness * np.sin(ac_rad)
    ext_start_y = spiral_lower_ends.start.y - thickness * np.cos(ac_rad)
    ext_end_x = spiral_lower_ends.end.x + thickness * np.sin(bc_rad)
    ext_end_y = spiral_lower_ends.end.y - thickness * np.cos(bc_rad)

    # bundle the coordinate components into the standard format
    ext_a_xy_1 = Coordinate(x=ext_start_x, y=ext_start_y)
    ext_a_xy_2 = Coordinate(x=spiral_upper_ends.start.x, y=spiral_upper_ends.start.y)
    ext_b_xy_1 = Coordinate(x=ext_end_x, y=ext_end_y)
    ext_b_xy_2 = Coordinate(x=spiral_upper_ends.end.x, y=spiral_upper_ends.end.y)

    # bundle the coordinates into the standard line format
    extension_ends_a = LineAttributes(start=ext_a_xy_1, end=ext_a_xy_2, line_type=LineType.LINE, name='extension_a')
    extension_ends_b = LineAttributes(start=ext_b_xy_1, end=ext_b_xy_2, line_type=LineType.LINE, name='extension_b')

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
    chamfer_a = LineAttributes(start=extension_ends_a.start, end=spiral_ends_lower.start, line_type=LineType.SEMICIRCLE, name='chamfer_start_a')
    chamfer_b = LineAttributes(start=spiral_ends_lower.end, end=extension_ends_b.start, line_type=LineType.SEMICIRCLE, name='chamfer_start_b')

    # Bundle the line and spiral coordinates into lists
    spiral_ends = [spiral_ends_lower, spiral_ends_upper]
    extension_ends = [extension_ends_a, extension_ends_b]
    fillet_ends = [chamfer_a, chamfer_b]

    return spiral_ends, extension_ends, fillet_ends