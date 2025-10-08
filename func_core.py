from func_helper import *
from class_logarithmic_spiral import LogarithmicSpiral

def generate_log_spiral_from_points(a_xy, b_xy, ac_deg, bc_deg, solver_accuracy, iter_limit, verbose):
    """Fits a logarithmic spiral to a start and end point at a given start and end angle"""
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
    """Fits a logarithmic spiral to a specific chhord and stretch at a given start and end angle"""
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


def generate_diffuser_from_geometry(inlet_width, outlet_width, thickness, stretch, chord, ac_deg, bc_deg,
                                    solver_accuracy, iter_limit, verbose):
    """Creates the goemetry of a curved diffuser from logarithmic spirals"""
    coordinates = diffuser_coordinates(inlet_width, outlet_width, stretch, chord)
    spirals = list()
    for coord in coordinates:
        name, a_xy, b_xy = coord
        s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg, name)
        s.calculate_tangent_geometry(a_xy, b_xy, ac_deg, bc_deg)
        s.validate_tangent_geometry()
        s.calculate_triangle_geometry()
        s.validate_triangle_geometry()
        s.calculate_origin_location(solver_accuracy, iter_limit, verbose=verbose)
        s.calculate_origin_offsets(inlet_width, outlet_width, thickness)
        spirals.append(s)
    print_diffuser_table(spirals)
    for spiral in spirals:
        print(spiral)
    save_diffuser(spirals, "./equations.csv")
    plot_diffuser(spirals)
