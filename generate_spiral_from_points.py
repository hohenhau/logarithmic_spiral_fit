# Fit logarithmic spirals to specific geometric properties

from func_core import spiral_calculator

# basic geometry parameters
A = (5, 0)                  # x & y coordinate of point A
B = (0, 4)                  # x & y coordinates of point B
AC_deg = 130                 # 4 quadrant angle of vector A in degrees
BC_deg = 180                # 4 quadrant angle of vector B in degrees

# simulation parameters
acc = 0.000000001           # solution accuracy
limit = 100                 # maximum number of iterations
verb = False                # change verbosity of script

# Execute core function
spiral_calculator(A, B, AC_deg, BC_deg, acc, limit)
