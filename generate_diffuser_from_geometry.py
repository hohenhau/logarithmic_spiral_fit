from func_core import generate_diffuser_from_geometry

# basic geometry parameters
ac_deg = 90     # 4 quadrant angle of vector A in degrees
bc_deg = 180    # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 141     # chord length of OUTER diffuser curve
stretch = 1  # stretch of CENTRAL curve (height / width)

# diffuser parameters
inlet_width = 20    # width of inlet
outlet_width = 40   # width of outlet

# simulation parameters
solver_accuracy = 0.000000001   # solution accuracy
iter_limit = 100                # maximum number of iterations
verbose = True                  # change verbosity of script

# Execute core function
generate_diffuser_from_geometry(inlet_width, outlet_width, stretch, chord, ac_deg, bc_deg,
                                solver_accuracy, iter_limit, verbose)