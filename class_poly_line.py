from copy import deepcopy

from class_line import Line
from class_coordinate import Coordinate
import matplotlib.pyplot as plt
import numpy as np
import math


class PolyLine:

    def __init__(self, xx=None, yy=None, zz=None, label=None, style='-'):
        """Initialises a PolyLine lass instance"""
        # Validate types
        for var_name, var_value in (('xx', xx), ('yy', yy), ('zz', zz)):
            if var_value is not None and not isinstance(var_value, list) and not isinstance(var_value, np.ndarray):
                raise TypeError(f"{var_name} must be a list or None, got {type(var_value).__name__}")
        # Validate lengths
        lists = [lst for lst in (xx, yy, zz) if lst is not None]
        if len(lists) > 1:
            length = len(lists[0])
            if not all(len(lst) == length for lst in lists):
                raise ValueError("All non-None coordinate lists (xx, yy, zz) must have the same length")
        # Assign attributes
        self.label = label
        self.style = style
        self.xx = xx
        self.yy = yy
        self.zz = zz


    def __repr__(self):
        return (f"PolyLine("
                f"label={self.label!r}, "
                f"style={self.style!r}, "
                f"start={self.xx[0], self.yy[0], self.zz[0]}, "
                f"end={self.xx[1], self.yy[1], self.zz[1]})")


    # ----- Instantiation Methods ------------------------------------------------------------------------------------ #


    @classmethod
    def generate_from_coordinate_list(cls, coordinates:list[Coordinate], label=None, style='-'):
        """Creates a PolyLine from a list of Coordinate objects."""
        xx, yy = [coord.x for coord in coordinates], [coord.y for coord in coordinates]
        return cls(xx=xx, yy=yy, label=label, style=style)


    @classmethod
    def generate_from_lists_of_floats(cls, xx:list[float], yy:list[float], label=None, style='-'):
        """Creates a PolyLine directly from separate lists of x and y floats."""
        return cls(xx=xx, yy=yy, label=label, style=style)


    @classmethod
    def generate_from_list_of_float_pairs(cls, pairs:list[tuple[float, float]], label=None, style='-'):
        """Creates a PolyLine from a list of (x, y) tuples."""
        xx, yy = [pair[0] for pair in pairs], [pair[1] for pair in pairs]
        return cls(xx=xx, yy=yy, label=label, style=style)


    # ----- Coordinate Generation ------------------------------------------------------------------------------------ #

    @staticmethod
    def generate_line_from_line(line:Line) -> tuple[list[float], list[float]]:
        """Generates a set of X and Y coordinates for a straight line"""
        xx = [line.start.x, line.end.x]
        yy = [line.start.y, line.end.y]
        return xx, yy


    @staticmethod
    def generate_semi_circle_from_coordinates(
            start:Coordinate,
            end:Coordinate,
            num_points=21,
            clockwise=False) -> tuple[list[float], list[float]]:
        """Generates a set of X and Y coordinates for a semicircular fillet"""
        # Ensure that number of points is odd to have a centred mid-point
        num_points = num_points if num_points % 2 != 0 else num_points + 1
        # Midpoint between start and end
        cx = (start.x + end.x) / 2
        cy = (start.y + end.y) / 2
        # Vector from start to end
        dx = end.x - start.x
        dy = end.y - start.y
        radius = math.sqrt(dx ** 2 + dy ** 2) / 2
        # Angle of start→end
        theta = math.atan2(dy, dx)
        # Generate semicircle angles
        if clockwise:
            angles = [theta + math.pi - i * math.pi / (num_points - 1) for i in range(num_points)]
        else:
            angles = [theta - math.pi + i * math.pi / (num_points - 1) for i in range(num_points)]
        # Compute coordinates
        xx = [cx + radius * math.cos(a) for a in angles]
        yy = [cy + radius * math.sin(a) for a in angles]
        return xx, yy


    # ----- Geometry Manipulation ------------------------------------------------------------------------------------ #

    def offset(self, x=0, y=0, z=0):
        """
        Offset the polyline coordinates by x, y, and z. Modifies in place but also returns self for chaining.
        """
        for axis_label, axis_offset in (('xx', x), ('yy', y), ('zz', z)):
            coordinates = getattr(self, axis_label)
            if coordinates is not None:
                coordinates = np.array(coordinates, dtype=float) + axis_offset
                setattr(self, axis_label, coordinates.tolist())
        return self


    def scale_all(self, scale_factor):
        """Takes a scale factor and applies it to all coordinates of the PolyLine. Return self for chaining."""
        self.xx = (np.array(self.xx) * scale_factor).tolist()
        self.yy = (np.array(self.yy) * scale_factor).tolist()
        self.zz = (np.array(self.zz) * scale_factor).tolist()
        return self


    def set_all_x(self, x_value):
        """Sets all X coordinates to a specified value. Returns self for chaining."""
        if self.xx is None and self.yy is None and self.zz is None:
            raise ValueError("Cannot set all X values if there are no existing coordinate values")
        length = max(len(self.yy), len(self.zz))
        self.xx = [x_value for _ in range(length)]
        return self


    def set_all_y(self, y_value):
        """Sets all Y coordinates to a specified value. Returns self for chaining."""
        if self.xx is None and self.yy is None and self.zz is None:
            raise ValueError("Cannot set all Y values if there are no existing coordinate values")
        length = max(len(self.xx), len(self.zz))
        self.yy = [y_value for _ in range(length)]
        return self


    def set_all_z(self, z_value):
        """Sets all Z coordinates to a specified value. Returns self for chaining."""
        if self.xx is None and self.yy is None and self.zz is None:
            raise ValueError("Cannot set all Z values if there are no existing coordinate values")
        length = max(len(self.xx), len(self.yy))
        self.zz = [z_value for _ in range(length)]
        return self


    # ----- Plotting and File Generation------------------------------------------------------------------------------ #

    def plot(self):
        """Plots the PolyLine on a matplotlib figure."""
        plt.plot(self.xx, self.yy, self.style, label=self.label)


    @staticmethod
    def calculate_face_normal(
            a_xyz:tuple[float, float, float],
            b_xyz:tuple[float, float, float],
            c_xyz:tuple[float, float, float]) -> tuple[float, float, float]:

        vector_ab = np.array(b_xyz) - np.array(a_xyz)
        vector_bc = np.array(c_xyz) - np.array(b_xyz)
        normal_vector = np.cross(vector_ab, vector_bc)
        normal_vector = normal_vector / np.linalg.norm(normal_vector)
        return normal_vector[0], normal_vector[1], normal_vector[2]


    @classmethod
    def create_stl_file_from_xy_poly_line(
            cls,
            poly_lines,
            height: float,
            file_directory: str,
            file_name=None,
            stl_scale=1.0,
            sig_figs=6
    ) -> None:
        """
        Converts one or more 2D PolyLines into a properly formatted ASCII STL file.

        Each PolyLine is extruded along Z by `height`, centered at z=0.
        Floating-point values are formatted in scientific notation with `sig_figs` digits.
        """

        # Wrap single PolyLine in list if necessary
        if isinstance(poly_lines, cls):
            poly_lines = [poly_lines]

        # Determine filename
        if file_name is None:
            file_name = poly_lines[0].label if hasattr(poly_lines[0], "label") else "unnamed"

        # Prepare format string for scientific notation
        fmt = f"{{:.{sig_figs}e}}"

        # Write STL file
        file_path = f"{file_directory}/{file_name}.stl"
        with open(file_path, "w") as f:
            f.write(f"solid {file_name}\n")

            for poly_line in poly_lines:
                # Validate polyline length
                if len(poly_line.xx) < 2 or len(poly_line.yy) < 2:
                    raise ValueError("PolyLine must have at least 2 points")

                # Create top and bottom layers
                poly_line_upper = deepcopy(poly_line).set_all_z(height / 2).scale_all(stl_scale)
                poly_line_lower = deepcopy(poly_line).set_all_z(-height / 2).scale_all(stl_scale)

                for i in range(len(poly_line_upper.xx) - 1):

                    # ----------------------------------------------------------------------------------------- #
                    # A --- D  Use the i and j indices to create a quadruplet of coordinates as on the left
                    # | \ / |  There should be two triangles: ABC and CDA
                    # |  X  |  These two triangles combined fill the rectangle ABCD
                    # | / \ |  By iterating over all quadruplets of coordinates, a full STL file is created
                    # B --- C  Each triangle also requires the computation of the facet normal
                    # ----------------------------------------------------------------------------------------- #

                    # Generate the index for the neighbouring coordinate
                    j = i + 1

                    # Extract coordinates
                    a_xyz = (poly_line_upper.xx[i], poly_line_upper.yy[i], poly_line_upper.zz[i])
                    b_xyz = (poly_line_lower.xx[i], poly_line_lower.yy[i], poly_line_lower.zz[i])
                    c_xyz = (poly_line_lower.xx[j], poly_line_lower.yy[j], poly_line_lower.zz[j])
                    d_xyz = (poly_line_upper.xx[j], poly_line_upper.yy[j], poly_line_upper.zz[j])


                    # Compute normals
                    abc_norm = cls.calculate_face_normal(a_xyz, b_xyz, c_xyz)
                    cda_norm = cls.calculate_face_normal(c_xyz, d_xyz, a_xyz)

                    # Helper for STL vertex and normal line formatting
                    def fmt_line(label, values):
                        return f"      {label} " + " ".join(fmt.format(v) for v in values) + "\n"

                    # Write two triangles (ABC, CDA)
                    for norm, tri in [
                        (abc_norm, [a_xyz, b_xyz, c_xyz]),
                        (cda_norm, [c_xyz, d_xyz, a_xyz]),
                    ]:
                        f.write(f"   facet normal {fmt.format(norm[0])} {fmt.format(norm[1])} {fmt.format(norm[2])}\n")
                        f.write("      outer loop\n")
                        for vertex in tri:
                            f.write(fmt_line("vertex", vertex))
                        f.write("      endloop\n")
                        f.write("   endfacet\n")

            f.write("endsolid\n")





