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
            if var_value is not None and not isinstance(var_value, list):
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


    @classmethod  # cls stands for class
    def generate_poly_line_from_line(cls, line:Line, reverse=False, name=None):
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
        return cls(xx=xx, yy=yy, label=name)


    @classmethod
    def generate_poly_line_from_lists_of_coordinates(cls, coordinates:list[Coordinate], label=None, style=None):
        """Creates a PolyLine from a list of Coordinate objects."""
        xx, yy = [coord.x for coord in coordinates], [coord.y for coord in coordinates]
        return cls(xx=xx, yy=yy, label=label, style=style)


    @classmethod
    def generate_poly_line_from_list_of_floats(cls, xx:list[float], yy:list[float], label=None, style=None):
        """Creates a PolyLine directly from separate lists of x and y floats."""
        return cls(xx=xx, yy=yy, label=label, style=style)


    @classmethod
    def generate_poly_line_from_list_of_coordinate_pairs(cls, pairs:list[tuple[float, float]], label=None, style=None):
        """Creates a PolyLine from a list of (x, y) tuples."""
        xx, yy = [pair[0] for pair in pairs], [pair[1] for pair in pairs]
        return cls(xx=xx, yy=yy, label=label, style=style)


    def plot(self):
        """Plots the PolyLine on a matplotlib figure."""
        plt.plot(self.xx, self.yy, self.style, label=self.label)
        

    def offset(self, x=0, y=0, z=0):
        """Offset the polyline coordinates by x, y, z using NumPy for element-wise addition."""
        for axis_name, axis_offset in (('xx', x), ('yy', y), ('zz', z)):
            axis_coordinates = getattr(self, axis_name)
            if axis_coordinates is not None:
                axis_coordinates = np.array(axis_coordinates, dtype=float) + axis_offset
                setattr(self, axis_name, axis_coordinates.tolist())

