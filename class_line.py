from enum import Enum
from class_coordinate import Coordinate
from class_logarithmic_spiral import LogarithmicSpiral

class Line:

    def __init__(
            self,
            start:Coordinate,
            end:Coordinate,
            label='',
            style='-') -> None:

        self.start = start
        self.end = end
        self.label = label
        self.style = style
        self.spiral = None
        self.spiral:LogarithmicSpiral


    def __repr__(self):
        return (f"Line("
                f"label={self.label!r}, "
                f"start={self.start}, "
                f"end={self.end})")


    def get_slope(self):
        """Returns the slope of the line based on the start and end coordinates"""
        rise = self.end.y - self.start.y
        run = self.end.x - self.start.x
        return rise / run


    def get_orientation(self):
        """Return (x, y) orientation of the line: -1, 0, or 1 along each axis."""
        x = int(self.end.x > self.start.x) - int(self.end.x < self.start.x)
        y = int(self.end.y > self.start.y) - int(self.end.y < self.start.y)
        return x, y