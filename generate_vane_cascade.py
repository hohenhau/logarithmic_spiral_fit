from PIL.ImageOps import scale

from func_core import generate_vane, generate_vane_cascade
from func_helper import save_cascade_characteristics

# basic geometry parameters
ac_deg = 90     # 4 quadrant angle of vector A in degrees
bc_deg = 120    # 4 quadrant angle of vector B in degrees
chord = 200     # chord length of OUTER diffuser curve
stretch = 4     # stretch of CENTRAL curve (height / width)
thickness = 2   # thickness of the vanes


# Cascade parameters
horizontal_pitch = 25               # vertical pitch of vanes
pitch_ratio = 1.55                  # Pitch ratios for expansion 1 and 2  are 1.55 and 1.72 respectively
vertical_pitch = horizontal_pitch * pitch_ratio  # horizontal pitch of vanes
num_vanes = 2                       # number of canes in the cascade
upstream_channel_length = 500       # upstream length of the channel
downstream_channel_length = 1000    # downstream length of the channel

# STL file parameters
file_directory = '/Users/alex/Desktop/expansionVanes'
stl_height = 100
stl_scale = 1/1000

# Recommended settings for 90 degree logarithmic vanes
if abs(bc_deg - ac_deg) == 90:
    suggested_g_t_c = 0.230  # This value comes from my PhD research
    suggested_chord = ((horizontal_pitch + thickness) ** 2 + (vertical_pitch + thickness) ** 2) ** 0.5 / suggested_g_t_c
    print(f'suggested chord is {suggested_chord} based on a gap-to-chord ratio of {suggested_g_t_c}')

vane_poly_line_and_ends = generate_vane(
    horizontal_pitch=horizontal_pitch,
    vertical_pitch=vertical_pitch,
    thickness=thickness,
    chord=chord,
    stretch=stretch,
    ac_deg=ac_deg,
    bc_deg=bc_deg)

generate_vane_cascade(
    horizontal_pitch=horizontal_pitch,
    vertical_pitch=vertical_pitch,
    ac_deg=ac_deg,
    bc_deg=bc_deg,
    upstream_channel_length=upstream_channel_length,
    downstream_channel_length=downstream_channel_length,
    vane_poly_line_and_ends=vane_poly_line_and_ends,
    num_vanes=num_vanes,
    file_directory=file_directory,
    stl_height=stl_height,
    stl_scale=stl_scale)

save_cascade_characteristics(
    horizontal_pitch=horizontal_pitch,
    vertical_pitch=vertical_pitch,
    chord=chord,
    stretch=stretch,
    scale=stl_scale,
    file_directory=file_directory)