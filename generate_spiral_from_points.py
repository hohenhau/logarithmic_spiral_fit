# Fit logarithmic spirals to specific geometric properties

from func_core import generate_log_spiral_from_points

# basic geometry parameters
a_xy = (4, 0)   # x & y coordinate of point A
b_xy = (0, 3)   # x & y coordinates of point B
ac_deg = 90     # 4 quadrant angle of vector A in degrees
bc_deg = 180    # 4 quadrant angle of vector B in degrees

# Execute core function
generate_log_spiral_from_points(a_xy=a_xy, b_xy=b_xy, ac_deg=ac_deg, bc_deg=bc_deg)
