from func_core import generate_vane

# vane parameters
horizontal_pitch = 25.0                           # vertical pitch of vanes
pitch_ratio = 1.55                                # pitch ratios for expansion 1 and 2  are 1.55 and 1.72 respectively
vertical_pitch = horizontal_pitch * pitch_ratio   # horizontal pitch of vanes
chord = 200                                       # chord length of vane
stretch = 3.26                                    # stretch of vane
thickness = 2                                      # thickness of the vanes
ac_deg = 90                                       # 4 quadrant angle of vector A in degrees
bc_deg = 120                                      # 4 quadrant angle of vector B in degrees

# Plotting and file parameters
show_plot=True
file_directory = "/Users/alex/Desktop/"


# Execute core function
vane = generate_vane(
    horizontal_pitch=horizontal_pitch,
    vertical_pitch=vertical_pitch,
    chord=chord,
    stretch=stretch,
    thickness=thickness,
    ac_deg=ac_deg,
    bc_deg=bc_deg,
    show_plot=show_plot,
    file_directory=file_directory)

