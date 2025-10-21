from copy import deepcopy

from class_line import Line
from class_coordinate import Coordinate
import matplotlib.pyplot as plt
import numpy as np
import math


class PolyLine:

    def __init__(self, xx=None, yy=None, zz=None, label=None, style='-'):
        """Initialises a PolyLine lass instance"""

        # Assign attributes
        self.label = label
        self.style = style
        self.xx = xx
        self.yy = yy
        self.zz = zz

        # Run validation checks
        self.validate_types()
        self.validate_lengths()


    def __len__(self):
        """Returns the length of the PolyLine instance components"""
        self.validate_lengths()
        len_x = len(self.xx) if self.xx is not None else 0
        len_y = len(self.yy) if self.yy is not None else 0
        len_z = len(self.zz) if self.zz is not None else 0
        return max(len_x, len_y, len_z)


    def __repr__(self):
        """Developer friendly string representation of the PolyLine instance"""
        return (f"PolyLine("
                f"label={self.label!r}, "
                f"style={self.style!r}, "
                f"start={self.xx[0], self.yy[0], self.zz[0]}, "
                f"end={self.xx[1], self.yy[1], self.zz[1]})")


    def __add__(self, other):
        """Adds two PolyLines or a PolyLine and a coordinate"""
        if isinstance(other, PolyLine):
            xx = self.xx + other.xx if self.xx is not None else other.xx
            yy = self.yy + other.yy if self.yy is not None else other.yy
            zz = self.zz + other.zz if self.zz is not None else other.zz
        elif isinstance(other, Coordinate):
            xx = self.xx + [other.x] if self.xx is not None else [other.x]
            yy = self.yy + [other.y] if self.yy is not None else [other.y]
            zz = self.zz + [other.z] if self.zz is not None else [other.z]
        else:
            raise ValueError(f"Cannot add {type(other)} to PolyLine")
        return PolyLine(xx=xx, yy=yy, zz=zz)


    def __getitem__(self, key):
        """Allows PolyLines to be slices like a normal list"""
        xx = self.xx[key] if self.xx is not None else None
        yy = self.yy[key] if self.yy is not None else None
        zz = self.zz[key] if self.zz is not None else None
        return type(self)(xx=xx, yy=yy, zz=zz)


    # ----- Validation Methods -------------------------------------------------------------------------------------- #

    def validate_types(self):
        """Checks that the coordinates are of type list or ndarray"""
        for var_name, var_value in (('xx', self.xx), ('yy', self.yy), ('zz', self.zz)):
            if var_value is not None and not isinstance(var_value, list) and not isinstance(var_value, np.ndarray):
                raise TypeError(f"{var_name} must be a list or None, got {type(var_value).__name__}")


    def validate_lengths(self):
        """Checks that the coordinate components are all equally long"""
        lists = [lst for lst in (self.xx, self.yy, self.zz) if lst is not None]
        if len(lists) > 1:
            length = len(lists[0])
            if not all(len(lst) == length for lst in lists):
                x_str = f'x_len = {len(self.xx)}, ' if self.xx else ''
                y_str = f'y_len = {len(self.yy)}, ' if self.yy else ''
                z_str = f'z_len = {len(self.zz)}' if self.zz else ''
                raise ValueError(f"Mismatched lengths: {x_str}{y_str}{z_str}")


    # ----- Instantiation Methods ----------------------------------------------------------------------------------- #


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


    # ----- Coordinate Generation ----------------------------------------------------------------------------------- #

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


    # ----- Geometry Manipulation ----------------------------------------------------------------------------------- #

    def offset_by_xyz(self, x: float | None = None, y: float | None = None, z: float | None = None):
        """Offset the polyline coordinates by x, y, and z. Modifies in place but also returns self for chaining."""
        for axis_label, axis_offset in (('xx', x), ('yy', y), ('zz', z)):
            coordinates = getattr(self, axis_label)
            if coordinates is None or axis_offset is None:
                continue
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


    def pop(self) -> Coordinate:
        """Pops the last items of all existing coordinate components, and returns the popped coordinate"""
        if self.xx is None and self.yy is None and self.zz is None:
            raise IndexError("Cannot pop and element. PolyLine has no coordinates")
        x = y = z = None
        if self.xx is not None:
            x = self.xx.pop()
        if self.yy is not None:
            y = self.yy.pop()
        if self.zz is not None:
            z = self.zz.pop()
        return Coordinate(x=x, y=y, z=z)


    # ----- Plotting and File Generation----------------------------------------------------------------------------- #

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
        normal_vector = (normal_vector / np.linalg.norm(normal_vector)).tolist()
        return normal_vector[0], normal_vector[1], normal_vector[2]


    @classmethod
    def create_stl_file_from_xy_poly_line(
            cls,
            poly_lines,
            height: float,
            file_directory: str,
            create_end_cap=False,
            file_name=None,
            stl_scale=1.0,
            sig_figs=6
    ) -> None:
        """
        Converts one or more 2D PolyLines into a properly formatted ASCII STL file.
        """

        # Wrap single PolyLine in list if necessary
        if isinstance(poly_lines, cls):
            poly_lines = [poly_lines]

        # Determine filename
        if file_name is None:
            file_name = poly_lines[0].label if hasattr(poly_lines[0], "label") else "unnamed"

        # Write STL file
        file_path = f"{file_directory}/{file_name}.stl"
        with open(file_path, "w") as f:
            f.write(f"solid {file_name}\n")

            for poly_line in poly_lines:
                # Validate polyline length
                if len(poly_line.xx) < 2 or len(poly_line.yy) < 2:
                    raise ValueError("PolyLine must have at least 2 points")

                # Create top and bottom layers
                line_pos = deepcopy(poly_line).set_all_z(height / 2).scale_all(stl_scale)
                line_neg = deepcopy(poly_line).set_all_z(-height / 2).scale_all(stl_scale)

                # Create vertical connection between line_1 and line_2
                f.write(cls.create_stl_vertices_between_lines(line_pos, line_neg, sig_figs))

                # End step if end caps should not be generated
                if not create_end_cap:
                    continue

                # Create end caps for line 1 and line 2
                print('Creating end caps')
                for line, reverse in [(line_pos, True), (line_neg, False)]:  # , (line_neg, True)
                    centre = len(line) // 2
                    half_1 = line[0:centre]
                    half_2 = line[centre:-1][::-1]
                    f.write(cls.create_stl_vertices_between_lines(half_1, half_2, sig_figs, reverse=reverse))

            f.write("endsolid\n")



    @classmethod
    def create_stl_vertices_between_lines(cls, line_1, line_2, sig_figs:float, reverse=False) -> str:
        """
        Generates STL facet vertex strings between two PolyLine instances.
        Floating-point values are formatted in scientific notation with `sig_figs` digits.
        """

        # Check validity of input
        if not isinstance(line_1, cls) or not isinstance(line_2, cls):
            raise TypeError(f"line_1 and line_2 must be of the type {cls}")
        elif abs(len(line_1) - len(line_2)) > 1:
            raise ValueError("Lines can differ in their number of coordinates by at most 1.")

        # Determine if end point requires special treatment
        if len(line_1) > len(line_2):
            odd_end = line_1.pop()
        elif len(line_2) > len(line_1):
            odd_end = line_2.pop()
        else:  # The lines are of equal length
            odd_end = None

        # Prepare format string for scientific notation
        fmt = f"{{:.{sig_figs}e}}"

        # Helper for STL vertex and normal line formatting
        def fmt_line(label, values):
            return f"      {label} " + " ".join(fmt.format(v) for v in values) + "\n"

        # Initialise string to contain vertices
        vertices = ''

        # ----------------------------------------------------------------------------------------- #
        #   A --- D   Use the i and j indices to create a quadruplet of coordinates as on the left
        #   | \ / |   There should be two triangles: ABC and CDA
        #   |  X  |   These two triangles combined fill the rectangle ABCD
        #   | / \ |   By iterating over all quadruplets of coordinates, a full STL file is created
        #   B --- C   Each triangle also requires the computation of the facet normal
        # ----------------------------------------------------------------------------------------- #

        for i in range(len(line_1.xx) - 1):
            # Generate the index for the neighbouring coordinate
            j = i + 1

            # Extract coordinates
            a_xyz = (line_1.xx[i], line_1.yy[i], line_1.zz[i])
            b_xyz = (line_2.xx[i], line_2.yy[i], line_2.zz[i])
            c_xyz = (line_2.xx[j], line_2.yy[j], line_2.zz[j])
            d_xyz = (line_1.xx[j], line_1.yy[j], line_1.zz[j])

            # Swap the coordinates to ensure normals point outwards
            if reverse:
                a_xyz, c_xyz = c_xyz, a_xyz


            # Compute normals
            abc_norm = cls.calculate_face_normal(a_xyz, b_xyz, c_xyz)
            cda_norm = cls.calculate_face_normal(c_xyz, d_xyz, a_xyz)

            # Write two triangles (ABC, CDA)
            for norm, tri in [(abc_norm, [a_xyz, b_xyz, c_xyz]), (cda_norm, [c_xyz, d_xyz, a_xyz])]:
                vertices += f"   facet normal {fmt.format(norm[0])} {fmt.format(norm[1])} {fmt.format(norm[2])}\n"
                vertices += "      outer loop\n"
                for vertex in tri:
                    vertices += (fmt_line("vertex", vertex))
                vertices += "      endloop\n"
                vertices += "   endfacet\n"

        # ----------------------------------------------------------------------------------------- #
        #    A      If the lines are of uneven length, the end point needs special treatment
        #    | \    We simply include it by closing it in the last triangle
        #    |  C   We access points A and B as the last elements in the line 1 and line 2 list
        #    | /    Once again the points are connected counter-clockwise (ABC)
        #    B      Note that this is intended for end caps of closed loop surfaces
        # ----------------------------------------------------------------------------------------- #

        if odd_end is not None:
            # Access the coordinates and generate the normal vector
            a_xyz = (line_1.xx[-1], line_1.yy[-1], line_1.zz[-1])
            b_xyz = (line_2.xx[-1], line_2.yy[-1], line_2.zz[-1])
            c_xyz = (odd_end.x, odd_end.y, odd_end.z)
            tri = [a_xyz, b_xyz, c_xyz]
            norm = cls.calculate_face_normal(a_xyz, b_xyz, c_xyz)

            # Write the end vertices to the output
            vertices += f"   facet normal {fmt.format(norm[0])} {fmt.format(norm[1])} {fmt.format(norm[2])}\n"
            vertices += "      outer loop\n"
            for vertex in tri:
                vertices += (fmt_line("vertex", vertex))
            vertices += "      endloop\n"
            vertices += "   endfacet\n"

        return vertices





