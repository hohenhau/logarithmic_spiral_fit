# Python script to estimate the parametric equations for a logarithmic spiral joining two arbitrary points
from copy import deepcopy

# section to import various standard libraries

import matplotlib.pyplot as plt     # import graphing library
import numpy as np                  # importing commonly used mathematical functions
import pandas as pd
from numpy import sqrt              # import various functions from numpy library
from class_line import *            # Import the line class


# ----- Additional Plotting Functions -------------------------------------------------------------------------------- #


def plot_xy_coordinates(x:list, y=None, style='-', label=None):
    """
    Plot a set of X and Y coordinates

    Parameters
    ----------
    x : list[float] | list[tuple[float, float]]
        X values, or a list of (x, y) coordinate pairs.
    y : list[float], optional
        Y values if x_or_points is a list of X values.
    """

    if y is None:  # Single list of (x, y)
        try:
            x, y = zip(*x)
        except (TypeError, ValueError):
            raise ValueError("If 'y' is not provided, 'x_or_points' must be a list of (x, y) pairs.")
    else:  # Separate x and y lists
        x = x
        if len(x) != len(y):
            raise ValueError("x and y must have the same length.")
    plt.plot(x, y, style, label=label)


def plot_graph_elements(
        title=None,
        x_label=None, y_label=None,
        min_x=None,
        max_x=None,
        min_y=None,
        max_y=None,
        file_name=None,
        file_directory=None):
    """Sets up a general line plot with optional attributes."""


    # Use the current figure and axes
    fig = plt.gcf()
    ax = plt.gca()

    # Set the fig width and fig height in mm
    fig_width_mm = 130
    fig_height_mm = 130

    # Convert figure sizes to inches
    inches_to_mm = 25.4
    fig_width_inches = fig_width_mm / inches_to_mm
    fig_height_inches = fig_height_mm / inches_to_mm
    fig.set_size_inches(fig_width_inches, fig_height_inches)

    # Set title and axis labels
    if title:
        ax.set_title(title, fontsize=10, linespacing=1)
    if x_label:
        ax.set_xlabel(x_label)
    if y_label:
        ax.set_ylabel(y_label)

    # Draw axes and grid
    ax.axhline(0, color='black', linewidth=0.8)
    ax.axvline(0, color='black', linewidth=0.8)
    ax.grid(True)

    # Only call legend if there are artists that could be put in the legend
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        ax.legend()

    # Current data limits
    x_lims = ax.get_xlim()
    y_lims = ax.get_ylim()

    # Compute defaults if None
    pad_ratio = 0.05
    if min_x is None: min_x = x_lims[0] - abs(x_lims[1] - x_lims[0]) * pad_ratio
    if max_x is None: max_x = x_lims[1] + abs(x_lims[1] - x_lims[0]) * pad_ratio
    if min_y is None: min_y = y_lims[0] - abs(y_lims[1] - y_lims[0]) * pad_ratio
    if max_y is None: max_y = y_lims[1] + abs(y_lims[1] - y_lims[0]) * pad_ratio

    # Apply limits
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)

    # Enforce equal scaling but preserve limits
    ax.set_aspect('equal', adjustable='box')

    if file_name and file_directory:
        file_location = f'{file_directory}/{file_name}'.replace('//', '/')
        print(f'saving file to {file_location}')
        fig.savefig(file_location, bbox_inches='tight', dpi=300)

    plt.show()



# ----- General Geometry Functions ----------------------------------------------------------------------------------- #

def calculate_points_from_chord(chord: float, stretch:float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Calculates the start and end coordinates of a spiral from the chord and the stretch"""
    a_x = sqrt(chord ** 2 / (stretch ** 2 + 1))
    b_y = stretch * a_x
    a, b = (a_x, 0), (0, b_y)
    return a, b


def find_intercept(
        coordinate_1:Coordinate,
        slope_1:float,
        coordinate_2:Coordinate,
        slope_2:float) -> Coordinate:
        """Function to find the intercept of two lines given their slope and a coordinate on the line"""

        # `Find the offset constant b for line 1
        x_1, y_1, a_1 = coordinate_1.x, coordinate_1.y, slope_1
        x_2, y_2, a_2 = coordinate_2.x, coordinate_2.y, slope_2

        # Set a verticality threshold
        verticality_threshold = 10e15

        if slope_1 == slope_2:  # Lines are parallel
            raise ValueError('Slopes are equal. The lines are parallel or coincident. No intercept can be found.')
        elif slope_1 > verticality_threshold and slope_2 > verticality_threshold:  # Both lines are vertical
            raise ValueError('Both slopes are vertical. No intercept can be found.')
        elif slope_1 > verticality_threshold:  # Line 1 is vertical
            x_3 = x_1
            b_2 = y_2 - slope_2 * x_2
            y_3 = slope_2 * x_3 + b_2
            return Coordinate(x=x_3, y=y_3)
        elif slope_2 > verticality_threshold:  # Line 2 is vertical
            x_3 = x_2
            b_1 = y_1 - slope_1 * x_1
            y_3 = slope_1 * x_3 + b_1
            return Coordinate(x=x_3, y=y_3)
        else:  # Neither line is vertical
            b_1 = y_1 - a_1 * x_1
            b_2 = y_2 - a_2 * x_2
            x_3 = (b_2 - b_1) / (a_1 - a_2)
            y_3 = a_1 * x_3 + b_1
            return Coordinate(x=x_3, y=y_3)


# ----- Diffuser Related Functions ----------------------------------------------------------------------------------- #

def diffuser_coordinates(
        inlet_width:float,
        outlet_width:float,
        stretch_centre:float,
        chord:float) -> list[Line]:
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
    ab_inner = Line(start=a_inner, end=b_inner, label='inner')

    # Define coordinates for centre spiral
    a_centre = Coordinate(x=a_x_centre, y=0)
    b_centre = Coordinate(x=0, y=b_y_centre)
    ab_centre = Line(start=a_centre, end=b_centre, label='centre', style='--')

    # Define coordinates for outer spiral
    a_outer = Coordinate(x=a_x_outer, y=0)
    b_outer = Coordinate(x=0, y=b_y_outer)
    ab_outer = Line(start=a_outer, end=b_outer, label='outer')

    # Calculate and print the stretch of the spirals to the console
    stretch_inner = b_y_inner / a_x_inner
    stretch_outer = b_y_outer / a_x_outer
    print("\nstretch of inner, centre, and outer curves respectively:")
    print(stretch_inner, stretch_centre, stretch_outer)

    return [ab_inner, ab_centre, ab_outer]

