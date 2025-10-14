class Coordinate:


    def __init__(self, x=None, y=None, z=None, name=None):
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


    def offset(self, x=0, y=0, z=0):
        """Offset the coordinate by x, y, z."""
        for axis_name, axis_offset in (('x', x), ('y', y), ('z', z)):
            value = getattr(self, axis_name)
            if value is not None:
                setattr(self, axis_name, value + axis_offset)