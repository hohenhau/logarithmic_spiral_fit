from func_core import generate_log_vane_from_geometry

# basic geometry parameters
ac_deg = 100     # 4 quadrant angle of vector A in degrees
bc_deg = 170    # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 100     # chord length of OUTER diffuser curve
stretch = 1  # stretch of CENTRAL curve (height / width)

# diffuser parameters
thickness = 2                   # thickness of the vanes
horizontal_pitch = 20    # width of inlet
vertical_pitch = 20   # width of outlet

# simulation parameters
solver_accuracy = 0.000000001   # solution accuracy
iter_limit = 100                # maximum number of iterations
verbose = True                  # change verbosity of script

# Recommended settings for 90 degree logarithmic vanes
if abs(bc_deg - ac_deg) == 90:
    suggested_gap_to_chord = 0.230  # This value comes from my PhD research
    suggested_chord = ((horizontal_pitch + thickness) ** 2 + (vertical_pitch + thickness) ** 2) ** 0.5 / suggested_gap_to_chord
    print(f'suggested chord is {suggested_chord} based on a gap-to-chord ratio of {suggested_gap_to_chord}')

# Execute core function
generate_log_vane_from_geometry(horizontal_pitch, vertical_pitch, thickness, chord, stretch, ac_deg, bc_deg,
                                solver_accuracy, iter_limit, verbose)