from func_helper import *
from class_logarithmic_spiral import LogarithmicSpiral, tabulate_spirals, save_spiral_equations

def generate_log_spiral_from_points(a_xy, b_xy, ac_deg, bc_deg, solver_accuracy, iter_limit, verbose):
    """Fits a logarithmic spiral to a start and end point at a given start and end angle"""
    s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg)
    s.calculate_tangent_geometry()
    s.validate_tangent_geometry()
    s.calculate_triangle_geometry()
    s.validate_triangle_geometry()
    s.calculate_origin_location(solver_accuracy, iter_limit, verbose=verbose)

    # Print the spiral equations
    print(s)

    # Create and plot the coordinates for the logarithmic spiral
    s_xx, s_yy = s.generate_graph_coordinates()
    plot_xy_coordinates(x_or_points=s_xx, y=s_yy, style='-', label='connector')

    # Create and plot the coordinates for a line connecting points A and B
    connecting_line = [a_xy, b_xy]
    plot_xy_coordinates(connecting_line, style='-o', label='connector')

    # Create and plot the coordinates for the tangent triangle
    tangent_triangle = [a_xy, s.c_xy, b_xy]
    plot_xy_coordinates(tangent_triangle, style='-o', label='tangent')

    # Create and plot the coordinates for the origin triangle
    origin_triangle = [a_xy, s.origin_xy, b_xy]
    plot_xy_coordinates(origin_triangle, style='-o', label='origin')

    # Plot the general graph elements (title, axis, etc.)
    plot_graph_elements()


def generate_log_spiral_from_chord(chord, stretch, ac_deg, bc_deg, solver_accuracy, iter_limit, verbose):
    """Fits a logarithmic spiral to a specific chord and stretch at a given start and end angle"""
    a_xy, b_xy = calculate_points_from_chord(chord, stretch)
    generate_log_spiral_from_points(a_xy, b_xy, ac_deg, bc_deg, solver_accuracy, iter_limit, verbose)


def generate_diffuser_from_geometry(inlet_width, outlet_width, stretch, chord, ac_deg, bc_deg,
                                    solver_accuracy, iter_limit, verbose):
    """Creates the geometry of a curved diffuser from logarithmic spirals"""
    coordinate_lines = diffuser_coordinates(inlet_width, outlet_width, stretch, chord)
    spirals = list()
    for line in coordinate_lines:
        a_xy = line.start.x, line.start.y
        b_xy = line.end.x, line.end.y
        s = LogarithmicSpiral(a_xy, b_xy, ac_deg, bc_deg, line.name)
        s.style = line.style
        s.calculate_tangent_geometry()
        s.validate_tangent_geometry()
        s.calculate_triangle_geometry()
        s.validate_triangle_geometry()
        s.calculate_origin_location(solver_accuracy, iter_limit, verbose=verbose)
        s.calculate_origin_offsets(inlet_width, outlet_width)
        spirals.append(s)
    tabulate_spirals(spirals)
    for s in spirals:
        print(s)
    for s in spirals:
        s_xx, s_yy = s.generate_graph_coordinates()
        plot_xy_coordinates(s_xx, s_yy, s.style, s.name)
    plot_graph_elements()
    save_spiral_equations(spirals, "./equations.csv")


def generate_log_vane_from_geometry(horizontal_pitch, vertical_pitch, thickness, chord, stretch, ac_deg, bc_deg,
                                    solver_accuracy, iter_limit, verbose):
    """Creates the geometry of a curved diffuser from logarithmic spirals"""

    # Generate spiral and line end coordinates from geometry
    spiral_ends, extension_ends, fillet_ends = log_vane_coordinates(
        horizontal_pitch, vertical_pitch, thickness,stretch, chord, ac_deg, bc_deg)

    spirals = list()
    for points in spiral_ends:
        points_start = points.start.x, points.start.y
        points_end = points.end.x, points.end.y
        s = LogarithmicSpiral(points_start, points_end, ac_deg, bc_deg, points.name)
        s.calculate_tangent_geometry()
        s.validate_tangent_geometry()
        s.calculate_triangle_geometry()
        s.validate_triangle_geometry()
        s.calculate_origin_location(solver_accuracy, iter_limit, verbose=verbose)
        s.calculate_origin_offsets(horizontal_pitch, vertical_pitch, thickness)
        spirals.append(s)
    tabulate_spirals(spirals)

    # Print the spiral equations to the console
    for s in spirals:
        print(s)

    # Save the spiral equations to the local directory
    save_spiral_equations(spirals, "./equations.csv")

    # Graph the coordinates of the spirals
    for s in spirals:
        x_s, y_s = s.generate_graph_coordinates()
        plot_xy_coordinates(x_s, y_s, s.style, s.name)

    # Graph coordinates the straight extensions
    for e in extension_ends:
        x_e, y_e = e.generate_graph_coordinates_line()
        plot_xy_coordinates(x_e, y_e, e.style, e.name)

    # Graph the coordinates of the filleted ends
    for f in fillet_ends:
        x_f, y_f = f.generate_graph_coordinates_semi_circle()
        plot_xy_coordinates(x_f, y_f, f.style, f.name)

    # Graph the other plot elements (title, axis, etc.)
    plot_graph_elements()

