# Fit logarithmic spirals to specific geometric properties

from log_spiral_func import *

# basic geometry parameters
A = (3, 0)                  # x & y coordinate of point A
B = (0, 4)                  # x & y coordinates of point B
AC_deg = 90                 # 4 quadrant angle of vector A in degrees
BC_deg = 180                # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 200              # chord length of OUTER diffuser curve
stretch = 0.70               # stretch of CENTRAL curve (height / width)

# diffuser parameters
thick = 2                   # thickness of the vanes
inlet = 21 - thick          # width of inlet
outlet = 42 - thick         # width of outlet

# simulation parameters
acc = 0.000000001           # solution accuracy
limit = 100                 # maximum number of iterations
verb = False                # change verbosity of script

spiral_calculator(A, B, AC_deg, BC_deg, acc, limit)
spiral_calculator_chord(chord, stretch, AC_deg, BC_deg, acc, limit)
diffuser_calculator(inlet, outlet, stretch, chord, AC_deg, BC_deg, thick, acc, limit)
