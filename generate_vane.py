from func_core import generate_vane

# basic geometry parameters
ac_deg = 90     # 4 quadrant angle of vector A in degrees
bc_deg = 180    # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 206     # chord length of OUTER diffuser curve
stretch = 0.7 # stretch of CENTRAL curve (height / width)

# vane parameters
thickness = 2           # thickness of the vanes
horizontal_pitch = 20    # width of inlet
vertical_pitch = 40     # width of outlet

# Plotting and file parameters
show_plot=True


# Execute core function
vane = generate_vane(
    horizontal_pitch=horizontal_pitch,
    vertical_pitch=vertical_pitch,
    chord=chord,
    stretch=stretch,
    thickness=thickness,
    ac_deg=ac_deg,
    bc_deg=bc_deg,
    show_plot=show_plot)

