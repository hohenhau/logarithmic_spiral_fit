from enum import Enum
from class_coordinate import Coordinate
from class_logarithmic_spiral import LogarithmicSpiral

class LineType(Enum):
    """Enumaration to define the types of lines"""
    LINE = "line"
    SPIRAL = "spiral"
    SEMICIRCLE = "semicircle"


class Line:

    def __init__(
            self,
            start:Coordinate,
            end:Coordinate,
            line_type=LineType.LINE,
            name='',
            style='-') -> None:

        self.start = start
        self.end = end
        self.name = name
        self.line_type = line_type
        self.style = style
        self.spiral = None
        self.spiral:LogarithmicSpiral


    def __repr__(self):
        return (f"Line("
                f"name={self.name!r}, "
                f"line_type={self.line_type.value!r}, "
                f"start={self.start}, "
                f"end={self.end})")