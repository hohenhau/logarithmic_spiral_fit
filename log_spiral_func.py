# Python script to estimate the parametric equations for a logarithmic spiral joining two arbitrary points


# section to import various standard libraries

import matplotlib.pyplot as plt                 # import graphing library
import numpy as np                              # importing commonly used mathematical functions
from numpy import pi, exp, sqrt, abs, round     # import various functions from numpy library
from numpy import cos, sin, tan                 # import various trigonometric functions
from numpy import degrees, radians              # import conversion functions
from numpy import arctan, arctan2               # importing the inverse and the 4 quadrant inverse tangent
from sys import exit


def chord_coordinates(chord, stretch):
    A_x = sqrt(chord ** 2 / (stretch ** 2 + 1))
    B_y = stretch * A_x
    A, B = (A_x, 0), (0, B_y)
    return A, B


def diffuser_coordinates(inlet, outlet, stretch_centre, chord):
    chord_c1 = 1 + 1 / stretch_centre ** 2                         # 1st chord coefficient
    chord_c2 = outlet + inlet / stretch_centre                     # 2nd chord coefficient
    chord_c3 = (inlet ** 2 + outlet ** 2) / 4 - chord ** 2  # 3rd chord coefficient
    B_y_centre = (sqrt(chord_c2 ** 2 - 4 * chord_c1 * chord_c3) - chord_c2) / (2 * chord_c1)
    B_y_inner = B_y_centre - outlet / 2
    B_y_outer = B_y_centre + outlet / 2
    A_x_centre = B_y_centre / stretch_centre
    A_x_inner = A_x_centre - inlet / 2
    A_x_outer = A_x_centre + inlet / 2
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


def geometry_check(AB_rad, AC_rad, BC_rad):
    if AC_rad == BC_rad:
        print("invalid geometry: angle at point 'A' is the same as angle at point 'B'")
    elif AC_rad == AB_rad:
        print("invalid geometry: angle at point 'A' is coincident with vector connecting the points")
    elif BC_rad == AB_rad:
        print("invalid geometry: angle at point 'B' is coincident with vector connecting the points")
    elif AB_rad - AC_rad > 0 and AB_rad - BC_rad > 0:
        print("either angle 'A' is too small or angle 'B' is too large for the given points")
    elif AB_rad - AC_rad < 0 and AB_rad - BC_rad < 0:
        print("either angle 'A' is too large or angle 'B' is too small for the given points")
    else:
        print("basic geometric requirements have been met")
        return
    exit()


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
        alpha = β - pi / 2                                  # polar tangential angle
        AD_rad = AC_rad + β                           # 4 quadrant angle of vector AD
        BD_rad = BC_rad + β                           # 4 quadrant angle of vector BD
        angleAA = abs(AD_rad - AB_rad)                # absolute value of angle AA
        angleBB = abs(AB_rad + pi - BD_rad)           # absolute value of angle BB
        angleD = pi - angleAA - angleBB                     # absolute value of angle D
        AD_len = AB_len * sin(angleBB) / sin(angleD)      # length of vector AD
        BD_len = AB_len * sin(angleAA) / sin(angleD)      # length of vector BD
        AD_x = cos(AD_rad) * AD_len           # x component of vector AD
        AD_y = sin(AD_rad) * AD_len           # y component of vector AD
        A_x, A_y = A                                                        # x & y components of coordinate A
        D_x, D_y = A_x + AD_x, A_y + AD_y                       # x & y components of coordinate D
        D = (D_x, D_y)                                                      # coordinate D
        b = growth * abs(tan(alpha))                                        # polar slope 'b'
        t_a = arctan((A_y - D_y) / (A_x - D_x))                             # polar angle t_a
        t_b = t_a + θ                                                   # polar angle t_b
        a = (A_x - D_x) / (exp(b * t_a) * cos(t_a))                         # spiral scaling factor
        segment_x = a * exp(b * t_b) * cos(t_b) + D_x                       # x component of spiral segment
        segment_y = a * exp(b * t_b) * sin(t_b) + D_y                       # y component of spiral segment
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
    y_offset = origin_y + (outlet + thick / cos(BC_dev) + inlet * tan(BC_dev)) * 1
    return x_offset, y_offset


def sf(num, fig):  # return significant figure
    return '{:g}'.format(float('{:.{p}g}'.format(num, p=fig)))


def diffuser_table(atrb):
    print()
    print("characteristic            |\t  sign\t|",   atrb[0][0], "\t|",     atrb[1][0], "|",       atrb[2][0])
    print("------------------------------------------------------------------------------------")
    print("horizontal spiral origin  |\t    x \t|\t", atrb[0][1], "\t\t|\t", atrb[1][1], "\t\t|\t", atrb[2][1])
    print("vertical spiral origin    |\t    y \t|\t", atrb[0][2], "\t\t|\t", atrb[1][2], "\t\t|\t", atrb[2][2])
    print("polar slope angle         |\talpha \t|\t", atrb[0][3], "\t\t|\t", atrb[1][3], "\t\t|\t", atrb[2][3])
    print("scaling factor            |\t    a \t|\t", atrb[0][4], "\t\t|\t", atrb[1][4], "\t\t|\t", atrb[2][4])
    print("polar slope               |\t    b \t|\t", atrb[0][5], "\t\t|\t", atrb[1][5], "\t\t|\t", atrb[2][5])
    print("polar coordinate at A     |\t  t_a \t|\t", atrb[0][6], "\t\t|\t", atrb[1][6], "\t\t|\t", atrb[2][6])
    print("polar coordinate at B     |\t  t_b \t|\t", atrb[0][7], "\t\t|\t", atrb[1][7], "\t\t|\t", atrb[2][7])


def spiral_equations(t_a, t_b, a, b, x_offset, y_offset):
    print()
    print(f"from {t_a} to {t_b}")
    print(f"inner spiral   x = {a} * exp({b} * t) * cos(t) + {x_offset}")
    print(f"inner spiral   y = {a} * exp({b} * t) * sin(t) + {y_offset}")


def diffuser_equations(spir, x_offset, y_offset):
    spiral_equations(spir[0][6], spir[0][7], spir[0][4], spir[0][5], x_offset, y_offset)    # inner
    spiral_equations(spir[1][6], spir[1][7], spir[1][4], spir[1][5], 0, 0)                  # centre
    spiral_equations(spir[2][6], spir[2][7], spir[2][4], spir[2][5], 0, 0)                  # outer


def save_diffuser(spir, x_offset, y_offset, file_name):
    with open(file_name, 'w', encoding='utf-8-sig') as file:
        x_0 = f"{spir[0][4]}*exp({spir[0][5]}*t)*cos(t)+{x_offset},"
        y_0 = f"{spir[0][4]}*exp({spir[0][5]}*t)*sin(t)+{y_offset},"
        lim_l_0 = f"{spir[0][6]},"
        lim_u_0 = f"{spir[0][7]}"
        x_2 = f"{spir[2][4]}*exp({spir[2][5]}*t)*cos(t)+{spir[2][1]},"
        y_2 = f"{spir[2][4]}*exp({spir[2][5]}*t)*sin(t)+{spir[2][2]},"
        lim_l_2 = f"{spir[2][6]},"
        lim_u_2 = f"{spir[2][7]}"
        row_1 = "x,y,lower_limit,upper_limit" + "\n"
        row_2 = y_0 + x_0 + lim_l_0 + lim_u_0 + "\n"
        row_3 = y_2 + x_2 + lim_l_2 + lim_u_2
        file.write(row_1)
        file.write(row_2)
        file.write(row_3)
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


def plot_diffuser(spir, A, B, C, D):
    plot_spiral(spir[0][6], spir[0][7], spir[0][4], spir[0][5], spir[0][1], spir[0][2], '-', 'inner spiral')
    plot_spiral(spir[1][6], spir[1][7], spir[1][4], spir[1][5], spir[1][1], spir[1][2], '--', 'central spiral')
    plot_spiral(spir[2][6], spir[2][7], spir[2][4], spir[2][5], spir[2][1], spir[2][2], '-', 'outer spiral')
    line1 = [A, B]
    triangle1 = [A, C, B]
    triangle2 = [A, D, B]
    plot_line(line1, '-o', 'connector')
    plot_line(triangle1, '-o', 'tangent')
    plot_line(triangle2, '-o', 'origin')
    plot_general()


def spiral_calculator(A, B, AC_deg, BC_deg, acc, limit):
    AB_len, AB_rad, AC_rad, BC_rad, BC_dev = spiral_geometry(A, B, AC_deg, BC_deg)
    geometry_check(AB_rad, AC_rad, BC_rad)
    C, β, β_min, β_max, θ, growth = triangle_geometry(AB_rad, AC_rad, BC_rad, AB_len, A)
    D, alpha, a, b, t_a, t_b = origin(AB_len, AB_rad, AC_rad, BC_rad, A, β, β_min, β_max, θ, growth, acc, limit)
    spiral_equations(t_a, t_b, a, b, 0, 0)
    plot_spiral(t_a, t_b, a, b, D[0], D[1], '-', 'spiral')
    line1 = [A, B]
    triangle1 = [A, C, B]
    triangle2 = [A, D, B]
    plot_line(line1, '-o', 'connector')
    plot_line(triangle1, '-o', 'tangent')
    plot_line(triangle2, '-o', 'origin')
    plot_general()


def spiral_calculator_chord(chord, stretch, AC_deg, BC_deg, acc, limit):
    A, B = chord_coordinates(chord, stretch)
    AB_len, AB_rad, AC_rad, BC_rad, BC_dev = spiral_geometry(A, B, AC_deg, BC_deg)
    geometry_check(AB_rad, AC_rad, BC_rad)
    C, β, β_min, β_max, θ, growth = triangle_geometry(AB_rad, AC_rad, BC_rad, AB_len, A)
    D, alpha, a, b, t_a, t_b = origin(AB_len, AB_rad, AC_rad, BC_rad, A, β, β_min, β_max, θ, growth, acc, limit)
    spiral_equations(t_a, t_b, a, b, 0, 0)
    plot_spiral(t_a, t_b, a, b, D[0], D[1], '-', 'spiral')
    line1 = [A, B]
    triangle1 = [A, C, B]
    triangle2 = [A, D, B]
    plot_line(line1, '-o', 'connector')
    plot_line(triangle1, '-o', 'tangent')
    plot_line(triangle2, '-o', 'origin')
    plot_general()


def diffuser_calculator(inlet, outlet, stretch, chord, AC_deg, BC_deg, thick, acc, limit):
    coordinates = diffuser_coordinates(inlet, outlet, stretch, chord)
    atrb, spir = [], []
    for coord in coordinates:
        name, A, B = coord
        AB_len, AB_rad, AC_rad, BC_rad, BC_dev = spiral_geometry(A, B, AC_deg, BC_deg, name)
        geometry_check(AB_rad, AC_rad, BC_rad)
        C, β, β_min, β_max, θ, growth = triangle_geometry(AB_rad, AC_rad, BC_rad, AB_len, A)
        D, alpha, a, b, t_a, t_b = origin(AB_len, AB_rad, AC_rad, BC_rad, A, β, β_min, β_max, θ, growth, acc, limit)
        x_offset, y_offset = offsets(D[0], D[1], inlet, outlet, thick, BC_dev)
        values_long = [name, D[0], D[1], alpha, a, b, t_a, t_b]
        values_rounded = [name, sf(D[0], 3), sf(D[1], 3), sf(alpha, 3), sf(a, 3), sf(b, 3), sf(t_a, 3), sf(t_b, 3)]
        atrb.append(values_rounded)
        spir.append(values_long)
    diffuser_table(atrb)
    diffuser_equations(spir, x_offset, y_offset)
    save_diffuser(spir, x_offset, y_offset, "./equations.csv")
    plot_diffuser(spir, A, B, C, D)