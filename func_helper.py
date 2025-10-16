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

