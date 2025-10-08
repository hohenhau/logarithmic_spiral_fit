from func_helper import *
from class_logarithmic_spiral import LogarithmicSpiral

def generate_log_spiral_from_points(a_xy, b_xy, ac_deg, bc_deg, solver_accuracy, iter_limit, verbose):
    s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg)
    s.calculate_tangent_geometry(a_xy, b_xy, ac_deg, bc_deg)
    s.validate_tangent_geometry()
    s.calculate_triangle_geometry()
    s.validate_triangle_geometry(solver_accuracy)
    s.calculate_origin_location(solver_accuracy, iter_limit, verbose=verbose)
    print(s)
    s.plot_spiral()
    line1 = [a_xy, b_xy]
    triangle1 = [a_xy, s.c_xy, b_xy]
    triangle2 = [a_xy, s.origin_xy, b_xy]
    plot_line(line1, '-o', 'connector')
    plot_line(triangle1, '-o', 'tangent')
    plot_line(triangle2, '-o', 'origin')
    plot_general()


def generate_log_spiral_from_chord(chord, stretch, ac_deg, bc_deg, solver_accuracy, iter_limit, verbose):
    a_xy, b_xy = calculate_points_from_chord(chord, stretch)
    s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg)
    s.calculate_tangent_geometry(a_xy, b_xy, ac_deg, bc_deg)
    s.validate_tangent_geometry()
    s.calculate_triangle_geometry()
    s.validate_triangle_geometry(solver_accuracy)
    s.calculate_origin_location(solver_accuracy, iter_limit, verbose=verbose)
    print(s)
    s.plot_spiral()
    line1 = [a_xy, b_xy]
    triangle1 = [a_xy, s.c_xy, b_xy]
    triangle2 = [a_xy, s.origin_xy, b_xy]
    plot_line(line1, '-o', 'connector')
    plot_line(triangle1, '-o', 'tangent')
    plot_line(triangle2, '-o', 'origin')
    plot_general()


def generate_diffuser_from_geometry(inlet, outlet, stretch, chord, ac_deg, bc_deg, thick, solver_accuracy, iter_limit, verbose):
    coordinates = diffuser_coordinates(inlet, outlet, stretch, chord)
    spirals = list()
    for coord in coordinates:
        name, a_xy, b_xy = coord
        s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg, name)
        s.calculate_tangent_geometry(a_xy, b_xy, ac_deg, bc_deg)
        s.validate_tangent_geometry()
        s.calculate_triangle_geometry()
        s.validate_triangle_geometry(solver_accuracy)
        s.calculate_origin_location(solver_accuracy, iter_limit, verbose=verbose)
        spirals.append(s)
    print_diffuser_table(spirals)
    for spiral in spirals:
        print(spiral)
    save_diffuser(spirals, "./equations.csv")
    plot_diffuser(spirals)

#
# def generate_diffuser_from_geometry(inlet, outlet, stretch, chord, ac_deg, bc_deg, thick, solver_accuracy, iter_limit):
#     coordinates = diffuser_coordinates(inlet, outlet, stretch, chord)
#     spirals = list()
#     for coord in coordinates:
#         name, a_xy, b_xy = coord
#         spiral = LogarithmicSpiral(name)
#         AB_len, AB_rad, AC_rad, BC_rad, BC_dev = calculate_spiral_construction_geometry(a_xy, b_xy, ac_deg, bc_deg, name)
#         check_input_and_output_angles(AB_rad, AC_rad, BC_rad)
#         C, β, β_min, β_max, θ, growth = triangle_geometry(AB_rad, AC_rad, BC_rad, AB_len, a_xy)
#         D, alpha, a, b, t_a, t_b = origin(AB_len, AB_rad, AC_rad, BC_rad, a_xy, β, β_min, β_max, θ, growth, solver_accuracy, iter_limit)
#         x_offset, y_offset = offsets(D[0], D[1], inlet, outlet, thick, BC_dev)
#         spiral.origin_x, spiral.s_x_orig = D[0], sf(D[0], 3)
#         spiral.origin_y, spiral.s_y_orig = D[1], sf(D[1], 3)
#         spiral.polar_angle, spiral.s_po_angle = alpha, sf(alpha, 3)
#         spiral.factor, spiral.s_factor = a, sf(a, 3)
#         spiral.polar_slope_b, spiral.s_po_slope = b, sf(b, 3)
#         spiral.polar_a, spiral.s_po_A = t_a, sf(t_a, 3)
#         spiral.polar_b, spiral.s_po_B = t_b, sf(t_b, 3)
#         spiral.x_offset, spiral.s_x_offset = x_offset, sf(x_offset, 3)
#         spiral.y_offset, spiral.s_y_offset = y_offset, sf(y_offset, 3)
#         spirals.append(spiral)
#
#     print_diffuser_table(spirals)
#     print_diffuser_equations(spirals)
#     save_diffuser(spirals, "./equations.csv")
#     plot_diffuser(spirals, a_xy, b_xy, C, D)