import matplotlib.pyplot as plt                 # import graphing library
import numpy as np                              # importing commonly used mathematical functions
from numpy import pi, exp, sqrt, abs            # import various functions from numpy library
from numpy import cos, sin, tan                 # import various trigonometric functions
from numpy import degrees, radians              # import conversion functions
from numpy import arctan, arctan2               # importing the inverse and the 4 quadrant inverse tangent


class LogarithmicSpiral:
    """Contains all relevant characteristics used to define and determine the shape of a logarithmic spiral."""


    def __init__(self, a_xy, b_xy, ac_deg, bc_deg, name='spiral'):
        """Initialises an instance of LogarithmicSpiral"""

        # Input characteristics and geometry
        self.name = name                # name of the spiral
        self.a_xy = a_xy                # X and Y coordinates at point A
        self.b_xy = b_xy                # X and Y coordinates at point B
        self.ac_deg = ac_deg            # 4-quadrant angle of Vector AC in degrees
        self.bc_deg = bc_deg            # 4-quadrant angle of Vector BC in degrees
        self.ac_rad = radians(ac_deg)   # 4-quadrant angle of vector AC in radians
        self.bc_rad = radians(bc_deg)   # 4-quadrant angle of vector BC in radians
        self.style = '-'                # Graphing line style of spiral

        # Geometric characteristics of the logarithmic spiral
        self.origin_xy = None       # X and Y coordinates of the origin
        self.origin_y = None        # vertical spiral origin
        self.x_offset = 0           # horizontal spiral origin
        self.y_offset = 0           # vertical spiral origin
        self.polar_a = None         # polar coordinate at A
        self.polar_b = None         # polar coordinate at B
        self.factor = None          # scaling factor
        self.growth = None          # Growth factor of spiral

        # Tangent geometry
        self.ab_len = None          # Length from point A to point B
        self.ab_rad = None          # 4-quadrant angle of vector AB in radians
        self.bc_dev = None          # Angular deviation of vector BC

        # Triangle geometry
        self.a_rad = None           # Angle at point A in radians
        self.b_rad = None           # Angle at point B in radians
        self.c_rad = None           # Angle at point C in radians
        self.c_xy = None            # X and Y Coordinates of point C
        self.theta = None           # angle change between coordinates in radians
        self.beta_min = None        # minimum incident angle 'β'
        self.beta_max = None        # maximum incident angle 'β'
        self.beta = None            # actual incident angle 'β'

        # Origin geometry
        self.alpha = None           # polar tangential angle
        self.scale_factor_a = None  # spiral scaling factor 'a'
        self.polar_slope_b = None   # polar slope 'b'
        self.t_a_rad = None         # polar angle t_a
        self.t_b_rad = None         # polar angle t_b


    def __str__(self):
        """Return a formatted string representation of the spiral"""

        def fmt(x):
            return f"{x:.3g}" if isinstance(x, (int, float)) else "None"

        return (
            f"\n{self.name} from t = {fmt(self.t_a_rad)} to t = {fmt(self.t_b_rad)}\n"
            f"x = {fmt(self.scale_factor_a)} * exp({fmt(self.polar_slope_b)} * t) * cos(t) + {fmt(self.x_offset)}\n"
            f"y = {fmt(self.scale_factor_a)} * exp({fmt(self.polar_slope_b)} * t) * sin(t) + {fmt(self.y_offset)}")


    def calculate_tangent_geometry(self):
        # Calculate connecting vector AB from start and end coordinates

        ab_x = self.b_xy[0] - self.a_xy[0]  # x component of vector AB (connecting points A and B)
        ab_y = self.b_xy[1] - self.a_xy[1]  # y component of vector AB (connecting points A and B)
        self.ab_len = sqrt(ab_x ** 2 + ab_y ** 2)  # length of vector AB (between points A and B)
        print(f"\nperforming calculations for {self.name} (height = {ab_y} and width = {ab_x})")

        # Calculate the 4-quadrant angle of vector AB in radians
        self.ab_rad = arctan2(ab_y, ab_x)
        ab_deg = degrees(self.ab_rad)

        # Calculate and display angle AB in degrees
        ab_deg = degrees(self.ab_rad)  # 4 quadrant angle of vector AB in degrees
        print(f"\nAngle AC = {self.ac_deg:.3g}, angle BC = {self.bc_deg:.3g}, and angle AB = {ab_deg:.3g}")


    def validate_tangent_geometry(self):
        """Checks if spiral can be computed based on the input and putput angles"""
        if self.ac_rad == self.bc_rad:
            raise ValueError("Invalid geometry: angle at point 'A' is the same as angle at point 'B'")
        elif self.ac_rad == self.ab_rad:
            raise ValueError("Invalid geometry: angle at point 'A' is coincident with vector connecting the points")
        elif self.bc_rad == self.ab_rad:
            raise ValueError("Invalid geometry: angle at point 'B' is coincident with vector connecting the points")
        elif self.ab_rad - self.ac_rad > 0 and self.ab_rad - self.bc_rad > 0:
            raise ValueError("Either angle 'A' is too small or angle 'B' is too large for the given points")
        elif self.ab_rad - self.ac_rad < 0 and self.ab_rad - self.bc_rad < 0:
            raise ValueError("Either angle 'A' is too large or angle 'B' is too small for the given points")
        else:
            print("basic geometric requirements have been met. Proceeding...")


    def calculate_triangle_geometry(self):
        """Calculates the geometry of the triangle used to construct a logarithmic spiral"""

        # Calculate the angles of the triangle at points a, b, and c
        self.a_rad = abs(self.ab_rad - self.ac_rad)  # calculate absolute value of angle A
        self.b_rad = abs(self.ab_rad - self.bc_rad)  # calculate absolute value of angle B
        self.c_rad = pi - abs(self.bc_rad - self.ac_rad)  # calculate value of angle C

        # Calculate the length of vectors AC and BC to determine the direction of the spiral
        ac_len = self.ab_len * sin(self.b_rad) / sin(self.c_rad)  # length of vector AC (between points A and C)
        bc_len = self.ab_len * sin(self.a_rad) / sin(self.c_rad)  # length of vector BC (between points B and C)
        self.growth = 1 if ac_len < bc_len else -1 # spiral is expanding clockwise

        # Calculate the X and Y coordinates of point C
        vector_ac_x = cos(self.ac_rad) * ac_len  # x component of vector AC (connecting points A and C)
        vector_ac_y = sin(self.ac_rad) * ac_len  # y component of vector AC (connecting points A and C)
        c_x = self.a_xy[0] + vector_ac_x  # x component of coordinate C
        c_y = self.a_xy[1] + vector_ac_y  # y component of coordinate C
        self.c_xy = (c_x, c_y)  # coordinate C

        # Calculate the minimum and maximum incident angle 'β'
        self.theta = self.bc_rad - self.ac_rad  # angle change between coordinates in radians
        self.beta_min = self.ab_rad - self.ac_rad  # minimum incident angle 'β'
        self.beta_max = self.ab_rad + pi - self.bc_rad  # maximum incident angle 'β'
        self.beta = (self.beta_min + self.beta_max) / 2  # actual incident angle 'β'


    def calculate_bd_vector_and_segment_length(self, beta):
        """Takes a guess at a possible origin given the current angle beta"""

        # Calculate the length of the vectors connecting points A and B to the guessed origin D
        ad_rad = self.ac_rad + beta  # 4 quadrant angle of vector AD
        bd_rad = self.bc_rad + beta  # 4 quadrant angle of vector BD
        abs_aa_rad = abs(ad_rad - self.ab_rad)  # absolute value of angle AA
        abs_bb_rad = abs(self.ab_rad + pi - bd_rad)  # absolute value of angle BB
        abs_d_rad = pi - abs_aa_rad - abs_bb_rad  # absolute value of angle D
        ad_len = self.ab_len * sin(abs_bb_rad) / sin(abs_d_rad)  # length of vector AD
        bd_len = self.ab_len * sin(abs_aa_rad) / sin(abs_d_rad)  # length of vector BD

        # Given the length of vectors AD and BD, calculate the position of the guessed origin D
        ad_x = cos(ad_rad) * ad_len  # x component of vector AD
        ad_y = sin(ad_rad) * ad_len  # y component of vector AD
        a_x, a_y = self.a_xy  # x & y components of coordinate A
        d_x = a_x + ad_x  # x components of coordinate D (the origin)
        d_y = a_y + ad_y  # y components of coordinate D (the origin)
        self.origin_xy = (d_x, d_y)  # X and Y coordinates of the origin

        # Calculate the polar, slope and the polar angles to points A and B
        self.alpha = beta - pi / 2  # polar tangential angle
        self.polar_slope_b = self.growth * abs(tan(self.alpha))  # polar slope 'b'
        self.t_a_rad = arctan((a_y - d_y) / (a_x - d_x))  # polar angle to coordinate A't_a'
        self.t_b_rad = self.t_a_rad + self.theta  # polar angle to coordinate B 't_b'
        self.scale_factor_a = (a_x - d_x) / (exp(self.polar_slope_b * self.t_a_rad) * cos(self.t_a_rad))  # factor 'a'

        # Calculate the X and y components of the spiral segment
        segment_x = self.scale_factor_a * exp(self.polar_slope_b * self.t_b_rad) * cos(self.t_b_rad) + d_x
        segment_y = self.scale_factor_a * exp(self.polar_slope_b * self.t_b_rad) * sin(self.t_b_rad) + d_y
        segment = sqrt((segment_x - d_x) ** 2 + (segment_y - d_y) ** 2)  # length of spiral segment
        return bd_len, segment


    def validate_triangle_geometry(self):
        """Checks if spiral can be computed based on the minimum and maximum angles of incidence (β_max & β_min)"""

        # Calculate the segment lengths at the minimum and maximum angles of incidence (beta)
        bd_len_min, seg_min = self.calculate_bd_vector_and_segment_length(self.beta_max - 0.01)
        bd_len_max, seg_max = self.calculate_bd_vector_and_segment_length(self.beta_min + 0.01)
        print(f'{self.name}')
        # If the segment is smaller than bd, angle beta needs to be decreased
        # If the segment is larger than bd, angle beta needs to be increased
        # If there is a valid solution:
        # - At beta_min, bd_len needs to be smaller than seg_min (beta_min cannot be decreased)
        # - At beta_max, bd_len needs to be larger than seg_max (beta_max cannot be increased)
        if bd_len_min < seg_min:
            raise RuntimeError(f'{self.name} cannot be fitted to these points. The turning angle is too small')
        if bd_len_max > seg_max:
            raise RuntimeError(f'{self.name} cannot be fitted to these points. The turning angle is too large')


    def calculate_origin_location(self, solver_accuracy, iter_limit, verbose=True):
        """Binary-search-style algorithm for finding the origin of a spiral"""

        count = 1
        while True:
            # Take a guess at a possible origin given the current angle beta
            bd_len, segment = self.calculate_bd_vector_and_segment_length(self.beta)

            # Check the accuracy of the guess and repeat calculation if necessary and possible
            if verbose:
                print(f"iteration = {count}, "
                      f"alpha = {self.alpha}, "
                      f"beta = {self.beta}, "
                      f"segment = {segment}, "
                      f"vectorBD = {bd_len}")
            if segment + solver_accuracy > bd_len > segment - solver_accuracy:
                print(f"achieved accurate solution after {count} iterations")
                break
            elif count == iter_limit:
                raise RuntimeError("Reached iteration limit. Geometry likely invalid")
            elif bd_len < segment:
                self.beta_min = self.beta
                self.beta = (self.beta_min + self.beta_max) / 2
                if verbose: print(f"increasing beta to be between {self.beta_min} and {self.beta_max}")
            elif bd_len > segment:
                self.beta_max = self.beta
                self.beta = (self.beta_min + self.beta_max) / 2
                if verbose: print(f"decreasing beta to be between {self.beta_min} and {self.beta_max}")
            else:
                raise RuntimeError("Computation error on iterative solution")
            count += 1


    def calculate_origin_offsets(self, inlet_width:float, outlet_width:float, thickness=0):
        """Calculates the offset of the spiral origin based on inlet and outlet dimensions"""
        bc_dev = self.bc_rad - pi  # Angular deviation between vector BC and the x-axis
        self.x_offset = self.origin_xy[0] + inlet_width + thickness
        self.y_offset = self.origin_xy[1] + (outlet_width + thickness / cos(bc_dev) + inlet_width * tan(bc_dev))


    def generate_graph_coordinates(self, num_points=400):
        t_values = np.linspace(self.t_a_rad, self.t_b_rad, num_points)  # evenly spaced values (beginning, end, steps)
        x_values = self.scale_factor_a * exp(self.polar_slope_b * t_values) * cos(t_values) + self.origin_xy[0]
        y_values = self.scale_factor_a * exp(self.polar_slope_b * t_values) * sin(t_values) + self.origin_xy[1]
        spiral_tuples = list(zip(x_values, y_values))  # turn coordinates into a list of tuples with zip
        spiral_values = np.array(spiral_tuples)
        x_trim = spiral_values[:, 0:1]
        y_trim = spiral_values[:, 1:]
        return x_trim, y_trim


# ----- Static Functions --------------------------------------------------------------------------------------------- #

def tabulate_spirals(spirals):
    """Print the spiral characteristics to the console in table format"""
    if not spirals:
        return

    def fmt(x):
        return f"{x:.3g}" if isinstance(x, (int, float)) else str(x)

    labels = [
        ("Horizontal origin", "x", lambda s: s.origin_xy[0]),
        ("Vertical origin", "y", lambda s: s.origin_xy[1]),
        ("Polar slope angle", "α", lambda s: s.alpha),
        ("Scaling factor", "a", lambda s: s.scale_factor_a),
        ("Polar slope", "b", lambda s: s.polar_slope_b),
        ("Polar coordinate (A)", "t_a", lambda s: s.t_a_rad),
        ("Polar coordinate (B)", "t_b", lambda s: s.t_b_rad),
        ("Horizontal offset", "", lambda s: s.x_offset),
        ("Vertical offset", "", lambda s: s.y_offset),
    ]

    header = ["Characteristic", "Symbol"] + [s.name for s in spirals]
    col_count = len(header)
    col_widths = [21, 6] + [13] * (col_count - 2)
    row_format = " | ".join(f"{{:<{w}}}" if i < 2 else f"{{:>{w}}}" for i, w in enumerate(col_widths))

    print()
    print(row_format.format(*header))
    print("-" * (sum(col_widths) + 3 * (col_count - 1)))

    for label, symbol, getter in labels:
        row = [label, symbol] + [fmt(getter(s)) for s in spirals]
        print(row_format.format(*row))


def save_spiral_equations(spirals, file_name):
    """Saves the various spiral equations to a csv file"""
    with open(file_name, 'w', encoding='utf-8-sig') as file:
        file.write("name,x,y,lower_limit,upper_limit" + "\n")
        for s in spirals:
            x = f"{s.scale_factor_a}*exp({s.polar_slope_b}*t)*cos(t)+{s.x_offset},"
            y = f"{s.scale_factor_a}*exp({s.polar_slope_b}*t)*sin(t)+{s.y_offset},"
            lim_l = f"{s.t_a_rad},"
            lim_u = f"{s.t_b_rad}"
            name = f'{s.name},'
            row = name + y + x + lim_l + lim_u + "\n"
            file.write(row)
    print(f"successfully exported equations")