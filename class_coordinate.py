from __future__ import annotations

import numpy as np


class Coordinate:


    def __init__(self, x=None, y=None, z=None, label=None):
        self.label = label
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
        return f"Coordinate(name={self.label!r}, {self._format_parts(use_repr=True)})"


    def __str__(self):
        return self._format_parts()


    def __sub__(self, other:Coordinate) -> list:
        """Effectively returns the distance vector between two coordinates"""
        components = list()
        if self.x is not None and other.x is not None:
            components.append(self.x - other.x)
        if self.y is not None and other.y is not None:
            components.append(self.y - other.y)
        if self.z is not None and other.z is not None:
            components.append(self.z - other.z)
        if len(components) == 0:
            raise ValueError('These coordinates have no compatible components')
        return components


    def offset_by_xyz(self, x:float=None, y:float=None, z:float=None):
        """Offset the coordinate by coordinate components. Modifies in place and returns self for chaining."""
        if self.x is not None and x is not None: self.x += x
        if self.y is not None and y is not None: self.y += y
        if self.z is not None and z is not None: self.z += z
        return self


    def offset_by_dist_and_angle(self, distance:float, polar_angle:float, plane='xy'):
        """Offsets coordinate in a plane by a distance and angle. Modifies in place & returns self for chaining."""

        if plane == 'xy':
            if self.x is None or self.y is None:
                raise ValueError("Coordinates must have x and y")
            self.x += distance * np.cos(polar_angle)
            self.y += distance * np.sin(polar_angle)
        elif plane == 'xz':
            if self.x is None or self.y is None:
                raise ValueError("Coordinates must have x and z")
            self.x += distance * np.cos(polar_angle)
            self.z += distance * np.sin(polar_angle)
        elif plane == 'yz':
            if self.x is None or self.y is None:
                raise ValueError("Coordinates must have y and z")
            self.y += distance * np.cos(polar_angle)
            self.z += distance * np.sin(polar_angle)
        else:
            raise ValueError(f"Invalid plane: {plane}")

        return self
