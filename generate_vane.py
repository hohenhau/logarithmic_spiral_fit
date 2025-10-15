from func_core import generate_vane, generate_vane_cascade

# basic geometry parameters
ac_deg = 140     # 4 quadrant angle of vector A in degrees
bc_deg = 180    # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 141.42135624     # chord length of OUTER diffuser curve
stretch = 1/3 # stretch of CENTRAL curve (height / width)

# vane parameters
thickness = 2           # thickness of the vanes
horizontal_pitch = 20    # width of inlet
vertical_pitch = 20     # width of outlet
channel_length = 200

# Recommended settings for 90 degree logarithmic vanes
if abs(bc_deg - ac_deg) == 90:
    suggested_g_t_c = 0.230  # This value comes from my PhD research
    suggested_chord = ((horizontal_pitch + thickness) ** 2 + (vertical_pitch + thickness) ** 2) ** 0.5 / suggested_g_t_c
    print(f'suggested chord is {suggested_chord} based on a gap-to-chord ratio of {suggested_g_t_c}')

# Execute core function
vane = generate_vane(
    horizontal_pitch=horizontal_pitch,
    vertical_pitch=vertical_pitch,
    thickness=thickness,
    chord=chord,
    stretch=stretch,
    ac_deg=ac_deg,
    bc_deg=bc_deg)
