from func_core import spiral_calculator_chord

# basic geometry parameters
A = (3, 0)                  # x & y coordinate of point A
B = (0, 4)                  # x & y coordinates of point B
AC_deg = 90                 # 4 quadrant angle of vector A in degrees
BC_deg = 180                # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 200                 # chord length of OUTER diffuser curve
stretch = 0.70              # stretch of CENTRAL curve (height / width)

# simulation parameters
acc = 0.000000001           # solution accuracy
limit = 100                 # maximum number of iterations
verb = False                # change verbosity of script

# Execute core function
spiral_calculator_chord(chord, stretch, AC_deg, BC_deg, acc, limit)
