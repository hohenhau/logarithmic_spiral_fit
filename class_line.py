from enum import Enum
import math

class LineType(Enum):
    LINE = "line"
    SPIRAL = "spiral"
    SEMICIRCLE = "semicircle"


class Coordinate:
    def __init__(self, name, x=None, y=None, z=None):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

    def _format_parts(self, use_repr=False):
        parts = []
        for value, label in zip([self.x, self.y, self.z], ["x", "y", "z"]):
            if value is not None:
                fmt = f"{label}={value!r}" if use_repr else f"{label}={value}"
                parts.append(fmt)
        return ", ".join(parts)

    def __repr__(self):
        return f"Coordinate(name={self.name!r}, {self._format_parts(use_repr=True)})"

    def __str__(self):
        return self._format_parts()


class LineCoordinates:


    def __init__(
            self,
            name: str,
            start:Coordinate,
            end:Coordinate,
            line_type: LineType,
            style='-') -> None:

        self.start = start
        self.end = end
        self.name = name
        self.line_type = line_type
        self.style = style


    def __repr__(self):
        return (f"Line("
                f"name={self.name!r}, "
                f"line_type={self.line_type.value!r}, "
                f"start={self.start}, "
                f"end={self.end})")


    def generate_graph_coordinates_line(self) -> tuple[list[float], list[float]]:
        x = [self.start.x, self.end.x]
        y = [self.start.y, self.end.y]
        return x, y


    def generate_graph_coordinates_semi_circle(self, num_points=10, clockwise=False) -> tuple[list[float], list[float]]:
        # Midpoint between start and end
        centroid_x = (self.start.x + self.end.x) / 2
        centroid_y = (self.start.y + self.end.y) / 2

        # Radius (half the distance between start and end)
        dx = self.end.x - self.start.x
        dy = self.end.y - self.start.y
        radius = math.sqrt(dx ** 2 + dy ** 2) / 2

        # Angle of the line connecting start to end
        base_angle = math.atan2(dy, dx)

        # Determine direction of semicircle sweep
        if clockwise:
            start_angle = base_angle + math.pi / 2
            end_angle = base_angle - math.pi / 2
        else:
            start_angle = base_angle - math.pi / 2
            end_angle = base_angle + math.pi / 2

        # Generate semicircle points
        angles = [start_angle + i * (end_angle - start_angle) / (num_points - 1) for i in range(num_points)]

        x = [centroid_x + radius * math.cos(a) for a in angles]
        y = [centroid_y + radius * math.sin(a) for a in angles]

        return x, y