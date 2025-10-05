from func_helper import *

def generate_log_spiral_from_points(A, B, AC_deg, BC_deg, acc, limit):
    AB_len, AB_rad, AC_rad, BC_rad, BC_dev = spiral_geometry(A, B, AC_deg, BC_deg)
    validate_input_and_output_angles(AB_rad, AC_rad, BC_rad)
    C, β, β_min, β_max, θ, growth = triangle_geometry(AB_rad, AC_rad, BC_rad, AB_len, A)
    D, alpha, a, b, t_a, t_b = origin(AB_len, AB_rad, AC_rad, BC_rad, A, β, β_min, β_max, θ, growth, acc, limit)
    print_spiral_equations(t_a, t_b, a, b, 0, 0)
    plot_spiral(t_a, t_b, a, b, D[0], D[1], '-', 'spiral')
    line1 = [A, B]
    triangle1 = [A, C, B]
    triangle2 = [A, D, B]
    plot_line(line1, '-o', 'connector')
    plot_line(triangle1, '-o', 'tangent')
    plot_line(triangle2, '-o', 'origin')
    plot_general()


def generate_log_spiral_from_chord(chord, stretch, AC_deg, BC_deg, acc, limit):
    A, B = calculate_points_from_chord(chord, stretch)
    AB_len, AB_rad, AC_rad, BC_rad, BC_dev = spiral_geometry(A, B, AC_deg, BC_deg)
    validate_input_and_output_angles(AB_rad, AC_rad, BC_rad)
    C, β, β_min, β_max, θ, growth = triangle_geometry(AB_rad, AC_rad, BC_rad, AB_len, A)
    D, alpha, a, b, t_a, t_b = origin(AB_len, AB_rad, AC_rad, BC_rad, A, β, β_min, β_max, θ, growth, acc, limit)
    print_spiral_equations(t_a, t_b, a, b, 0, 0)
    plot_spiral(t_a, t_b, a, b, D[0], D[1], '-', 'spiral')
    line1 = [A, B]
    triangle1 = [A, C, B]
    triangle2 = [A, D, B]
    plot_line(line1, '-o', 'connector')
    plot_line(triangle1, '-o', 'tangent')
    plot_line(triangle2, '-o', 'origin')
    plot_general()


def generate_diffuser_from_geometry(inlet, outlet, stretch, chord, AC_deg, BC_deg, thick, acc, limit):
    coordinates = diffuser_coordinates(inlet, outlet, stretch, chord)
    spirals = list()
    for coord in coordinates:
        name, A, B = coord
        AB_len, AB_rad, AC_rad, BC_rad, BC_dev = spiral_geometry(A, B, AC_deg, BC_deg, name)
        validate_input_and_output_angles(AB_rad, AC_rad, BC_rad)
        C, β, β_min, β_max, θ, growth = triangle_geometry(AB_rad, AC_rad, BC_rad, AB_len, A)
        D, alpha, a, b, t_a, t_b = origin(AB_len, AB_rad, AC_rad, BC_rad, A, β, β_min, β_max, θ, growth, acc, limit)
        x_offset, y_offset = offsets(D[0], D[1], inlet, outlet, thick, BC_dev)
        spiral = LogarithmicSpiral(name)
        spiral.x_orig, spiral.s_x_orig = D[0], sf(D[0], 3)
        spiral.y_orig, spiral.s_y_orig = D[1], sf(D[1], 3)
        spiral.po_angle, spiral.s_po_angle = alpha, sf(alpha, 3)
        spiral.factor, spiral.s_factor = a, sf(a, 3)
        spiral.po_slope, spiral.s_po_slope = b, sf(b, 3)
        spiral.po_A, spiral.s_po_A = t_a, sf(t_a, 3)
        spiral.po_B, spiral.s_po_B = t_b, sf(t_b, 3)
        spiral.x_offset, spiral.s_x_offset = x_offset, sf(x_offset, 3)
        spiral.y_offset, spiral.s_y_offset = y_offset, sf(y_offset, 3)
        spirals.append(spiral)

    print_diffuser_table(spirals)
    diffuser_equations(spirals)
    save_diffuser(spirals, "./equations.csv")
    plot_diffuser(spirals, A, B, C, D)