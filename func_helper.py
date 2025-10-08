# Python script to estimate the parametric equations for a logarithmic spiral joining two arbitrary points


# section to import various standard libraries

import matplotlib.pyplot as plt                 # import graphing library
import numpy as np                              # importing commonly used mathematical functions
from numpy import sqrt                          # import various functions from numpy library


# ----- Additional Plotting Functions -------------------------------------------------------------------------------- #


def plot_line(points, style, label):
    """Plots a simple straight line"""
    line = np.array(points)
    x, y = line[:, 0:1], line[:, 1:]
    plt.plot(x, y, style, label=label)


def plot_general():
    """The basis for a general line plot"""
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axhline(0, color='black')   # x = 0
    plt.axvline(0, color='black')   # y = 0
    plt.grid()
    plt.show()


# ----- Diffuser Related Functions ----------------------------------------------------------------------------------- #


def calculate_points_from_chord(chord: float, stretch:float) -> tuple[tuple[float, float], tuple[float, float]]:
    """Calculates the start and end coordinates of a spiral from the chord and the stretch"""
    a_x = sqrt(chord ** 2 / (stretch ** 2 + 1))
    b_y = stretch * a_x
    a, b = (a_x, 0), (0, b_y)
    return a, b


def diffuser_coordinates(inlet_width:float, outlet_width:float, stretch_centre:float, chord:float):
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
    coordinates = [["inner spiral", a_inner, b_inner],
                   ["centre spiral", a_centre, b_centre],
                   ["outer spiral", a_outer, b_outer]]
    return coordinates


def print_diffuser_table(spirals):
    """Print the spiral characteristics to the console in table format"""
    s1, s2, s3 = spirals

    def fmt(x):
        return f"{x:.3g}" if isinstance(x, (int, float)) else str(x)

    data = [
        ("Horizontal origin",    "x",   fmt(s1.origin_xy[0]),   fmt(s2.origin_xy[0]),   fmt(s3.origin_xy[0])),
        ("Vertical origin",      "y",   fmt(s1.origin_xy[1]),   fmt(s2.origin_xy[1]),   fmt(s3.origin_xy[1])),
        ("Polar slope angle",    "α",   fmt(s1.alpha),          fmt(s2.alpha),          fmt(s3.alpha)),
        ("Scaling factor",       "a",   fmt(s1.scale_factor_a), fmt(s2.scale_factor_a), fmt(s3.scale_factor_a)),
        ("Polar slope",          "b",   fmt(s1.polar_slope_b),  fmt(s2.polar_slope_b),  fmt(s3.polar_slope_b)),
        ("Polar coordinate (A)", "t_a", fmt(s1.t_a_rad),        fmt(s2.t_a_rad),        fmt(s3.t_a_rad)),
        ("Polar coordinate (B)", "t_b", fmt(s1.t_b_rad),        fmt(s2.t_b_rad),        fmt(s3.t_b_rad)),
        ("Horizontal offset",    "",    fmt(s1.x_offset),       fmt(s2.x_offset),       fmt(s3.x_offset)),
        ("Vertical offset",      "",    fmt(s1.y_offset),       fmt(s2.y_offset),       fmt(s3.y_offset)),
    ]

    header = ("Characteristic", "Symbol", s1.name, s2.name, s3.name)
    row_format = "{:<21} | {:<6} | {:>13} | {:>13} | {:>13}"

    print()
    print(row_format.format(*header))
    print("-" * 78)
    for row in data:
        print(row_format.format(*row))


def save_diffuser(spirals, file_name):
    with open(file_name, 'w', encoding='utf-8-sig') as file:
        file.write("name,x,y,lower_limit,upper_limit" + "\n")
        for s in spirals:
            x = f"{s.scale_factor_a}*exp({s.polar_slope_b}*t)*cos(t)+{s.x_offset},"
            y = f"{s.scale_factor_a}*exp({s.polar_slope_b}*t)*sin(t)+{s.y_offset},"
            lim_l = f"{s.t_a_rad},"
            lim_u = f"{s.t_b_rad}"
            name = f'{s.name},'
            row = name + y + x + lim_l + lim_u + "\n"
            file.write(row)
    print(f"successfully exported equations")


def plot_diffuser(spirals):
    s1, s2, s3 = spirals
    s1.plot_spiral()
    s2.plot_spiral()
    s3.plot_spiral()
    plot_general()
