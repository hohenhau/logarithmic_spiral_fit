from copy import deepcopy

from class_line import Line, LineType
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

    @classmethod  # cls stands for class
    def generate_from_line(cls, line:Line, reverse=False, label=None):
        """Creates a PolyLine from a Line based on the LineType."""
        if line.line_type == LineType.LINE:
            xx, yy = cls.generate_line_from_line(line)
        elif line.line_type == LineType.SEMICIRCLE:
            xx, yy = cls.generate_semi_circle_from_line(line)
        elif line.line_type == LineType.SPIRAL:
            xx, yy = cls.generate_spiral_from_line(line)
        else:
            raise ValueError(f"LineType {line.line_type} not supported")
        if reverse:
            xx = xx[::-1]
            yy = yy[::-1]
        return cls(xx=xx, yy=yy, label=label)


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
    def generate_semi_circle_from_line(line:Line, num_points=21, clockwise=False) -> tuple[list[float], list[float]]:
        """Generates a set of X and Y coordinates for a semicircular fillet"""
        # Ensure that number of points is odd to have a centred mid-point
        num_points = num_points if num_points % 2 != 0 else num_points + 1
        # Midpoint between start and end
        cx = (line.start.x + line.end.x) / 2
        cy = (line.start.y + line.end.y) / 2
        # Vector from start to end
        dx = line.end.x - line.start.x
        dy = line.end.y - line.start.y
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


    @staticmethod
    def generate_spiral_from_line(line:Line) -> tuple[list[float], list[float]]:
        """Generates a set of X and Y coordinates for a spiral"""
        if line.spiral is None:
            raise ValueError("Spiral is to generate coordinates required")
        xx, yy = line.spiral.generate_spiral_coordinates()
        return xx, yy


    # ----- Geometry Manipulation ------------------------------------------------------------------------------------ #

    def offset(self, x=0, y=0, z=0):
        """
        Offset the polyline coordinates by x, y, and z. Modifies in place but also returns self for chaining.
        """
        for axis_label, axis_offset in (('xx', x), ('yy', y), ('zz', z)):
            coords = getattr(self, axis_label)
            if coords is not None:
                coords = np.array(coords, dtype=float) + axis_offset
                setattr(self, axis_label, coords.tolist())
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
            height:float,
            file_directory:str,
            file_name=None,
            scale=1.0,
            sig_figs=6) -> None:
        """Turns a 2-D PolyLine into an STL file"""

        # Check if the input is a PolyLine that is not wrapped in a list
        if isinstance(poly_lines, cls):
            poly_lines = [poly_lines]

        # Ensure that the file is assigned a name
        if file_name is None:
            file_name = poly_lines[0].label

        # Create a new or overwrite and exisitng file at the specified location
        with open(f"{file_directory}/{file_name}.stl", "w") as f:

            # Write file header
            f.write(f'solid {file_name}\n')

            # Iterate over the various bodies represented by the PolyLines
            for poly_line in poly_lines:

                # Check that the PolyLine is of sufficient length
                if len(poly_line.xx) < 2 or len(poly_line.yy) < 2:
                    raise ValueError("PolyLine must have at least 2 points")

                # Copy and offset the PolyLine to match the specified height
                poly_line_upper = deepcopy(poly_line).set_all_z(height / 2)
                poly_line_lower = deepcopy(poly_line).set_all_z(-height / 2)

                # Create body
                for i in range(len(poly_line_upper.xx) - 1):

                    # ----------------------------------------------------------------------------------------- #
                    # A --- D     Use the i and j indices to create a quadruplet of coordinates as on the left
                    # | \  /|     There should be two triangles: ABC and CDA
                    # |  X  |     These two triangles combined fill the rectangle ABCD
                    # | / \ |     By iterating over all quadruplets of coordinates, a full STL file is created
                    # B --- C     Each triangle also requires the computation of the facet normal
                    # ----------------------------------------------------------------------------------------- #

                    j = i + 1

                    # Extract the points a, b, c, and d
                    a_xyz = poly_line_upper.xx[i], poly_line_upper.yy[i], poly_line_upper.zz[i]
                    b_xyz = poly_line_lower.xx[i], poly_line_lower.yy[i], poly_line_lower.zz[i]
                    c_xyz = poly_line_lower.xx[j], poly_line_lower.yy[j], poly_line_lower.zz[j]
                    d_xyz = poly_line_upper.xx[j], poly_line_upper.yy[j], poly_line_upper.zz[j]

                    abc_norm = cls.calculate_face_normal(a_xyz, b_xyz, c_xyz)
                    cda_norm = cls.calculate_face_normal(c_xyz, d_xyz, a_xyz)

                    f.write(f'   facet normal {abc_norm[0]} {abc_norm[1]} {abc_norm[2]}\n')
                    f.write(f'      outer loop\n')
                    f.write(f'         vertex {a_xyz[0]} {a_xyz[1]} {a_xyz[2]}\n')
                    f.write(f'         vertex {b_xyz[0]} {b_xyz[1]} {b_xyz[2]}\n')
                    f.write(f'         vertex {c_xyz[0]} {c_xyz[1]} {c_xyz[2]}\n')
                    f.write(f'      endloop\n')
                    f.write(f'   endfacet\n')
                    f.write(f'   facet normal {cda_norm[0]} {cda_norm[1]} {cda_norm[2]}\n')
                    f.write(f'      outer loop\n')
                    f.write(f'         vertex {c_xyz[0]} {c_xyz[1]} {c_xyz[2]}\n')
                    f.write(f'         vertex {d_xyz[0]} {d_xyz[1]} {d_xyz[2]}\n')
                    f.write(f'         vertex {a_xyz[0]} {a_xyz[1]} {a_xyz[2]}\n')
                    f.write(f'      endloop\n')
                    f.write(f'   endfacet\n')

            # Write file footer
            f.write(f'endsolid\n')





