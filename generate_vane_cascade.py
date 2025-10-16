from func_core import generate_vane_cascade


# basic geometry parameters
ac_deg = 90     # 4 quadrant angle of vector A in degrees
bc_deg = 120    # 4 quadrant angle of vector B in degrees
chord = 200     # chord length of OUTER diffuser curve
stretch = 8.1     # stretch of CENTRAL curve (height / width)
thickness = 2   # thickness of the vanes

# Cascade parameters
horizontal_pitch = 25               # vertical pitch of vanes
pitch_ratio = 1.55                  # Pitch ratios for expansion 1 and 2  are 1.55 and 1.72 respectively
vertical_pitch = horizontal_pitch * pitch_ratio  # horizontal pitch of vanes
num_vanes = 2                       # number of canes in the cascade
upstream_channel_length = 500       # upstream length of the channel
downstream_channel_length = 1000    # downstream length of the channel

# STL file and plotting parameters
file_directory = '/Users/alex/Desktop/expansionVanes'
stl_height = 100
stl_scale = 1/1000   # To convert mm to m
show_plot = True

vane = generate_vane_cascade(
    horizontal_pitch=horizontal_pitch,
    vertical_pitch=vertical_pitch,
    chord=chord,
    stretch=stretch,
    thickness=thickness,
    ac_deg=ac_deg,
    bc_deg=bc_deg,
    upstream_channel_length=upstream_channel_length,
    downstream_channel_length=downstream_channel_length,
    num_vanes=num_vanes,
    file_directory=file_directory,
    stl_height=stl_height,
    stl_scale=stl_scale,
    show_plot=show_plot)


