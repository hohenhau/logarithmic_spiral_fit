# Python script to estimate the parametric equations for a logarithmic spiral joining two arbitrary points


# section to import various standard libraries

import matplotlib.pyplot as plt                 # import graphing library
import numpy as np                              # importing commonly used mathematical functions
from numpy import pi, exp, sqrt, abs, round     # import various functions from numpy library
from numpy import cos, sin, tan                 # import various trigonometric functions
from numpy import degrees, radians              # import conversion functions
from numpy import arctan, arctan2               # importing the inverse and the 4 quadrant inverse tangent
from sys import exit


class LogarithmicSpiral:
    def __init__(self, name):
        self.name = name  # name of the spiral
        self.style = '-'

        # Geometric characteristics of the logarithmic spiral
        self.x_orig = None      # horizontal spiral origin
        self.y_orig = None      # vertical spiral origin
        self.x_offset = 0       # horizontal spiral origin
        self.y_offset = 0       # vertical spiral origin
        self.po_slope = None    # polar slope
        self.po_angle = None    # polar slope angle
        self.po_A = None        # polar coordinate at A
        self.po_B = None        # polar coordinate at B
        self.factor = None      # scaling factor

        # Rounded geometric characteristics of the logarithmic spiral
        self.s_x_orig = None    # horizontal spiral origin
        self.s_y_orig = None    # vertical spiral origin
        self.s_x_offset = None  # horizontal spiral origin
        self.s_y_offset = None  # vertical spiral origin
        self.s_po_slope = None  # polar slope
        self.s_po_angle = None  # polar slope angle
        self.s_po_A = None      # polar coordinate at A
        self.s_po_B = None      # polar coordinate at B
        self.s_factor = None    # scaling factor

        # Construction geometry
        self.ab_len = None      # Length from point A to point B
        self.ab_rad = None      # 4 quadrant angle of vector AB in radians
        self.ac_rad = None      # 4 quadrant angle of vector AC in radians
        self.bc_rad = None      # 4 quadrant angle of vector BC in radians
        self.bc_dev = None      # Angular deviation of vector BC



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
    B_y_centre = (sqrt(chord_c2 ** 2 - 4 * chord_c1 * chord_c3) - chord_c2) / (2 * chord_c1)
    B_y_inner = B_y_centre - outlet_width / 2
    B_y_outer = B_y_centre + outlet_width / 2
    A_x_centre = B_y_centre / stretch_centre
    A_x_inner = A_x_centre - inlet_width / 2
    A_x_outer = A_x_centre + inlet_width / 2
    stretch_inner = B_y_inner / A_x_inner
    stretch_outer = B_y_outer / A_x_outer
    B_inner, B_centre, B_outer = (0, B_y_inner), (0, B_y_centre), (0, B_y_outer)
    A_inner, A_centre, A_outer = (A_x_inner, 0), (A_x_centre, 0), (A_x_outer, 0)
    print("\nstretch of inner, centre, and outer curves respectively:")
    print(stretch_inner, stretch_centre, stretch_outer)
    coordinates = [["inner spiral", A_inner, B_inner],
                   ["centre spiral", A_centre, B_centre],
                   ["outer spiral", A_outer, B_outer]]
    return coordinates


def spiral_geometry(A, B, AC_deg, BC_deg, name='spiral'):
    AB_x = B[0] - A[0]                      # x component of vector AB (connecting points A and B)
    AB_y = B[1] - A[1]                      # y component of vector AB (connecting points A and B)
    AB_len = sqrt(AB_x ** 2 + AB_y ** 2)    # length of vector AB (between points A and B)
    AB_rad = arctan2(AB_y, AB_x)            # 4 quadrant angle of vector AB in radians
    AB_deg = degrees(AB_rad)                # 4 quadrant angle of vector AB in degrees
    AC_rad = radians(AC_deg)                # 4 quadrant angle of vector A in radians
    BC_rad = radians(BC_deg)                # 4 quadrant angle of vector B in radians
    BC_dev = radians(BC_deg - 180)          # angular deviation
    print(f"\nperforming calculations for {name} (height = {B[1]} and width = {A[0]})")
    print(f"\nvector AC angle = {sf(AC_deg, 3)}, vector BC angle = {sf(BC_deg, 3)},"
          f" and vector AB angle = {sf(AB_deg, 3)}")
    return AB_len, AB_rad, AC_rad, BC_rad, BC_dev


def validate_input_and_output_angles(AB_rad, AC_rad, BC_rad):
    """Checks if spiral can be computed based on the input and putput angles"""
    if AC_rad == BC_rad:
        raise ValueError("Invalid geometry: angle at point 'A' is the same as angle at point 'B'")
    elif AC_rad == AB_rad:
        raise ValueError("Invalid geometry: angle at point 'A' is coincident with vector connecting the points")
    elif BC_rad == AB_rad:
        raise ValueError("Invalid geometry: angle at point 'B' is coincident with vector connecting the points")
    elif AB_rad - AC_rad > 0 and AB_rad - BC_rad > 0:
        raise ValueError("Either angle 'A' is too small or angle 'B' is too large for the given points")
    elif AB_rad - AC_rad < 0 and AB_rad - BC_rad < 0:
        raise ValueError("Either angle 'A' is too large or angle 'B' is too small for the given points")
    else:
        print("basic geometric requirements have been met")
        return


def triangle_geometry(AB_rad, AC_rad, BC_rad, AB_len, A):
    angleA = abs(AB_rad - AC_rad)                   # calculate absolute value of angle A
    angleB = abs(AB_rad - BC_rad)                   # calculate absolute value of angle B
    angleC = pi - abs(BC_rad - AC_rad)              # calculate value of angle C
    AC_len = AB_len * sin(angleB) / sin(angleC)     # length of vector AC (between points A and C)
    BC_len = AB_len * sin(angleA) / sin(angleC)     # length of vector BC (between points B and C)
    growth = 1                                      # spiral is expanding clockwise
    if AC_len > BC_len:                             # determine if there is a contraction or expansion
        growth = -1                                 # spiral is contracting clockwise
    vectorAC_x = cos(AC_rad) * AC_len               # x component of vector AC (connecting points A and C)
    vectorAC_y = sin(AC_rad) * AC_len               # y component of vector AC (connecting points A and C)
    C_x = A[0] + vectorAC_x                         # x component of coordinate C
    C_y = A[1] + vectorAC_y                         # y component of coordinate C
    C = (C_x, C_y)                                  # coordinate C
    θ = BC_rad - AC_rad                             # angle change between coordinates in radians
    β_min = AB_rad - AC_rad                         # minimum incident angle 'beta'
    β_max = AB_rad + pi - BC_rad                    # maximum incident angle 'beta'
    β = (β_min + β_max) / 2                         # actual incident angle 'beta'

    return C, β, β_min, β_max, θ, growth


def origin(AB_len, AB_rad, AC_rad, BC_rad, A, β, β_min, β_max, θ, growth, acc, limit):

    count = 1
    while True:
        alpha = β - pi / 2                              # polar tangential angle
        AD_rad = AC_rad + β                             # 4 quadrant angle of vector AD
        BD_rad = BC_rad + β                             # 4 quadrant angle of vector BD
        angleAA = abs(AD_rad - AB_rad)                  # absolute value of angle AA
        angleBB = abs(AB_rad + pi - BD_rad)             # absolute value of angle BB
        angleD = pi - angleAA - angleBB                 # absolute value of angle D
        AD_len = AB_len * sin(angleBB) / sin(angleD)    # length of vector AD
        BD_len = AB_len * sin(angleAA) / sin(angleD)    # length of vector BD
        AD_x = cos(AD_rad) * AD_len                     # x component of vector AD
        AD_y = sin(AD_rad) * AD_len                     # y component of vector AD
        A_x, A_y = A                                    # x & y components of coordinate A
        D_x, D_y = A_x + AD_x, A_y + AD_y               # x & y components of coordinate D
        D = (D_x, D_y)                                  # coordinate D
        b = growth * abs(tan(alpha))                    # polar slope 'b'
        t_a = arctan((A_y - D_y) / (A_x - D_x))         # polar angle t_a
        t_b = t_a + θ                                   # polar angle t_b
        a = (A_x - D_x) / (exp(b * t_a) * cos(t_a))     # spiral scaling factor
        segment_x = a * exp(b * t_b) * cos(t_b) + D_x   # x component of spiral segment
        segment_y = a * exp(b * t_b) * sin(t_b) + D_y   # y component of spiral segment
        segment = sqrt((segment_x - D_x) ** 2 + (segment_y - D_y) ** 2)     # length of spiral segment

        verb = True
        if verb:
            print(f"iteration = {count}, alpha = {alpha}, beta = {β}, segment = {segment}, vectorBD = {BD_len}")
        if segment + acc > BD_len > segment - acc:
            print(f"achieved accurate solution after {count} iterations")
            break
        elif count == limit:
            if verb: print("reached iteration limit, geometry likely to be invalid")
            exit()
        elif segment > BD_len:
            β_min = β
            β = (β_min + β_max) / 2
            if verb: print(f"increasing beta to be between {β_min} and {β_max}")
        elif segment < BD_len:
            β_max = β
            β = (β_min + β_max) / 2
            if verb: print(f"decreasing beta to be between {β_min} and {β_max}")
        else:
            print("computation error on iterative solution")
            exit()
        count += 1

    return D, alpha, a, b, t_a, t_b


def offsets(origin_x, origin_y, inlet, outlet, thick, BC_dev):
    x_offset = origin_x + inlet + thick
    y_offset = origin_y + (outlet + thick / cos(BC_dev) + inlet * tan(BC_dev))
    return x_offset, y_offset


def sf(num, fig):  # return significant figure
    return '{:g}'.format(float('{:.{p}g}'.format(num, p=fig)))


def print_diffuser_table(spirals):
    """ Print the spiral characteristics to the console in table format"""
    s1, s2, s3 = spirals

    data = [
        ("Horizontal origin",    "x",       s1.s_x_orig,    s2.s_x_orig,    s3.s_x_orig),
        ("Vertical origin",      "y",       s1.s_y_orig,    s2.s_y_orig,    s3.s_y_orig),
        ("Polar slope angle",    "α",       s1.s_po_angle,  s2.s_po_angle,  s3.s_po_angle),
        ("Scaling factor",       "a",       s1.s_factor,    s2.s_factor,    s3.s_factor),
        ("Polar slope",          "b",       s1.s_po_slope,  s2.s_po_slope,  s3.s_po_slope),
        ("Polar coordinate (A)", "tₐ",      s1.s_po_A,      s2.s_po_A,      s3.s_po_A),
        ("Polar coordinate (B)", "t_b",     s1.s_po_B,      s2.s_po_B,      s3.s_po_B),
        ("Horizontal offset",    "",        s1.s_x_offset,  s2.s_x_offset,  s3.s_x_offset),
        ("Vertical offset",      "",        s1.s_y_offset,  s2.s_y_offset,  s3.s_y_offset)]

    header = ("Characteristic", "Symbol", s1.name, s2.name, s3.name)

    row_format = "{:<21} | {:<6} | {:>13} | {:>13} | {:>12}"
    print()
    print(row_format.format(*header))
    print("-" * 77)
    for row in data:
        print(row_format.format(*row))

def print_spiral_equations(t_a, t_b, a, b, x_offset, y_offset, name='spiral'):
    """Prints the spiral equations to the console"""
    print()
    print(f"{name} from {t_a} to {t_b}")
    print(f"x = {a} * exp({b} * t) * cos(t) + {x_offset}")
    print(f"y = {a} * exp({b} * t) * sin(t) + {y_offset}")


def diffuser_equations(spirals):
    """Prints the three spiral equations from the diffuser to the console"""
    s1, s2, s3, = spirals
    print_spiral_equations(s1.po_A, s1.po_B, s1.factor, s1.po_slope, s1.x_offset, s1.y_offset, s1.name)
    print_spiral_equations(s2.po_A, s2.po_B, s2.factor, s2.po_slope, s2.x_offset, s2.y_offset, s2.name)
    print_spiral_equations(s3.po_A, s3.po_B, s3.factor, s3.po_slope, s3.x_offset, s3.y_offset, s3.name)


def save_diffuser(spirals, file_name):
    with open(file_name, 'w', encoding='utf-8-sig') as file:
        file.write("name,x,y,lower_limit,upper_limit" + "\n")
        for s in spirals:
            x = f"{s.factor}*exp({s.po_slope}*t)*cos(t)+{s.x_offset},"
            y = f"{s.factor}*exp({s.po_slope}*t)*sin(t)+{s.y_offset},"
            lim_l = f"{s.po_A},"
            lim_u = f"{s.po_B}"
            name = f'{s.name},'
            row = name + y + x + lim_l + lim_u + "\n"
            file.write(row)
    print(f"successfully exported equations")


def plot_spiral(t_a, t_b, a, b, origin_x, origin_y, style, label):
    step = (t_b - t_a) / 400
    t_values = np.arange(t_a, t_b, step)                       # evenly spaced values (beginning, end, step size)
    x_values = a * exp(b * t_values) * cos(t_values) + origin_x
    y_values = a * exp(b * t_values) * sin(t_values) + origin_y
    spiral_tuples = list(zip(x_values, y_values))             # turn coordinates into a list of tuples with zip
    spiral_values = np.array(spiral_tuples)
    X_trim = spiral_values[:, 0:1]
    Y_trim = spiral_values[:, 1:]
    plt.plot(X_trim, Y_trim, style, label=label)


def plot_line(points, style, label):
    line = np.array(points)
    x, y = line[:, 0:1], line[:, 1:]
    plt.plot(x, y, style, label=label)


def plot_general():
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.axhline(0, color='black')   # x = 0
    plt.axvline(0, color='black')   # y = 0
    plt.grid()
    plt.show()


def plot_diffuser(spirals, A, B, C, D):
    s1, s2, s3 = spirals
    plot_spiral(s1.po_A, s1.po_B, s1.factor, s1.po_slope, s1.x_orig, s1.y_orig, '-', s1.name)
    plot_spiral(s2.po_A, s2.po_B, s2.factor, s2.po_slope, s2.x_orig, s2.y_orig, '--', s2.name)
    plot_spiral(s3.po_A, s3.po_B, s3.factor, s3.po_slope, s3.x_orig, s3.y_orig, '-', s1.name)
    line1 = [A, B]
    triangle1 = [A, C, B]
    triangle2 = [A, D, B]
    plot_line(line1, '-o', 'connector')
    plot_line(triangle1, '-o', 'tangent')
    plot_line(triangle2, '-o', 'origin')
    plot_general()