# Fit logarithmic spirals to specific geometric properties

from func_core import generate_log_spiral_from_points

# basic geometry parameters
a_xy = (4, 0)                  # x & y coordinate of point A
b_xy = (0, 3)                  # x & y coordinates of point B
ac_deg = 90                 # 4 quadrant angle of vector A in degrees
bc_deg = 180                # 4 quadrant angle of vector B in degrees

# simulation parameters
solver_accuracy = 0.000000001           # solution accuracy
iter_limit = 100                 # maximum number of iterations
verbose = True                # change verbosity of script

# Execute core function
generate_log_spiral_from_points(a_xy, b_xy, ac_deg, bc_deg, solver_accuracy, iter_limit, verbose)
