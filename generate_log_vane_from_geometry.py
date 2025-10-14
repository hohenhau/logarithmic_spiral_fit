from func_core import generate_vane_from_geometry, generate_vane_cascade_from_vane

# basic geometry parameters
ac_deg = 80     # 4 quadrant angle of vector A in degrees
bc_deg = 190    # 4 quadrant angle of vector B in degrees

# chord parameters
chord = 200     # chord length of OUTER diffuser curve
stretch = 2  # stretch of CENTRAL curve (height / width)

# vane parameters
thickness = 2           # thickness of the vanes
horizontal_pitch = 5    # width of inlet
vertical_pitch = 40     # width of outlet
channel_length = 100

# Recommended settings for 90 degree logarithmic vanes
if abs(bc_deg - ac_deg) == 90:
    suggested_g_t_c = 0.230  # This value comes from my PhD research
    suggested_chord = ((horizontal_pitch + thickness) ** 2 + (vertical_pitch + thickness) ** 2) ** 0.5 / suggested_g_t_c
    print(f'suggested chord is {suggested_chord} based on a gap-to-chord ratio of {suggested_g_t_c}')

# Execute core function
vane = generate_vane_from_geometry(horizontal_pitch, vertical_pitch, thickness, chord, stretch, ac_deg, bc_deg)
generate_vane_cascade_from_vane(horizontal_pitch, vertical_pitch, ac_deg, bc_deg, channel_length, vane, num_vanes=2)