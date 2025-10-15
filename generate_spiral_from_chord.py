from func_core import generate_log_spiral_from_chord

# geometry parameters
ac_deg = 90         # 4 quadrant angle of vector A in degrees
bc_deg = 180        # 4 quadrant angle of vector B in degrees
chord = 100         # chord length of OUTER diffuser curve
stretch = 0.75      # stretch of CENTRAL curve (height / width)

# simulation parameters
solution_accuracy = 0.000000001  # solution accuracy
iteration_limit = 100            # maximum number of iterations
verbose = True                   # change verbosity of script

# Execute core function
generate_log_spiral_from_chord(chord=chord, stretch=stretch, ac_deg=ac_deg, bc_deg=bc_deg)
