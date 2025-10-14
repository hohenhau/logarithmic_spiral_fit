from func_core import generate_diffuser_from_geometry

# basic geometry parameters
ac_deg = 90     # 4 quadrant angle of vector A in degrees
bc_deg = 180    # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 141.4     # chord length of OUTER diffuser curve
stretch = 1  # stretch of CENTRAL curve (height / width)

# diffuser parameters
inlet_width = 20    # width of inlet
outlet_width = 40   # width of outlet

# Execute core function
generate_diffuser_from_geometry(inlet_width, outlet_width, stretch, chord, ac_deg, bc_deg)