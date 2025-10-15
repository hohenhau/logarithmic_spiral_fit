from __future__ import annotations

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


    def __sub__(self, other:Coordinate) -> tuple[float, float, float]:
        """Effectively returns the distance vector between two coordinates"""
        return self.x - other.x, self.y - other.y, self.z - other.z


    def offset(self, x=0, y=0, z=0):
        """Offset the coordinate in place and return self for chaining."""
        if self.x is not None: self.x += x
        if self.y is not None: self.y += y
        if self.z is not None: self.z += z
        return self