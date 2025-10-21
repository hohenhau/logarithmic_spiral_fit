import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
from func_helper import plot_graph_elements

from class_logarithmic_spiral import LogarithmicSpiral
from class_line import Line
from class_poly_line import PolyLine
from class_coordinate import Coordinate
from func_helper import find_intercept


class LogarithmicVane:

    def __init__(
            self,
            horizontal_pitch: float,
            vertical_pitch: float,
            thickness: float,
            chord_lower: float,
            stretch_lower: float,
            ac_deg: float,
            bc_deg: float,
            z_height: float = None,
            gap: float = None,
    ):

        # Basic Attributes
        self.horizontal_pitch = horizontal_pitch
        self.vertical_pitch = vertical_pitch
        self.chord_lower = chord_lower
        self.thickness = thickness
        self.stretch_lower = stretch_lower
        self.ac_deg = ac_deg
        self.bc_deg = bc_deg
        self.gap = gap
        self.z_height = z_height

        # Convert angle input to radians
        self.ac_rad = np.radians(ac_deg)
        self.bc_rad = np.radians(bc_deg)

        # Logarithmic Vane Coordinates
        self.lower_spiral_a:Coordinate | None = None
        self.lower_spiral_b:Coordinate | None = None
        self.upper_spiral_a:Coordinate | None = None
        self.upper_spiral_b:Coordinate | None = None
        self.extension_a:Coordinate | None = None
        self.extension_b:Coordinate | None = None
        self.end_point_a:Coordinate | None = None
        self.end_point_b:Coordinate | None = None

        # Logarithmic Vane PolyLines
        self.pl_lower_spiral:PolyLine | None = None
        self.pl_upper_spiral:PolyLine | None = None
        self.pl_extension_a:PolyLine | None = None
        self.pl_extension_b:PolyLine | None = None
        self.pl_fillet_a:PolyLine | None = None
        self.pl_fillet_b:PolyLine | None = None
        self.pl_outline:PolyLine | None = None

        # Generate the vane using the class methods
        self.make_suggestion()
        self.calculate_spiral_coordinates()
        self.check_extension_orientation()
        self.calculate_poly_lines_for_spirals()
        self.calculate_poly_lines_for_extensions()
        self.calculate_fillets_and_end_points()
        self.calculate_poly_outline()
        self.calculate_gap()
        self.calculate_pitch_angle()

    def get_all_poly_lines(self) -> list[PolyLine]:
        return [self.pl_lower_spiral, self.pl_upper_spiral,
                self.pl_extension_a, self.pl_extension_b,
                self.pl_fillet_a, self.pl_fillet_b,
                self.pl_outline]

    def get_all_coordinates(self) -> list[Coordinate]:
        return [self.lower_spiral_a, self.lower_spiral_b,
                self.upper_spiral_a, self.upper_spiral_b,
                self.extension_a, self.extension_b,
                self.end_point_a, self.end_point_b]


    def make_suggestion(self):
        # Recommended settings for 90 degree logarithmic vanes
        if abs(self.bc_deg - self.ac_deg) == 90:
            suggested_g_t_c = 0.230  # This value comes from my PhD research
            suggested_chord = ((self.horizontal_pitch + self.thickness) ** 2 + (
                    self.vertical_pitch + self.thickness) ** 2) ** 0.5 / suggested_g_t_c
            print(f'suggested chord is {suggested_chord} based on a gap-to-chord ratio of {suggested_g_t_c}')


    def calculate_spiral_coordinates(self):
        """Calculates the chord lines of the various components that make up a logarithmic turning vane"""

        # Calculate the chord line for the lower vane surface
        lower_width = self.chord_lower / np.sqrt(self.stretch_lower**2 + 1)
        lower_height = self.stretch_lower * lower_width

        self.lower_spiral_a = Coordinate(x=lower_width, y=0)
        self.lower_spiral_b = Coordinate(x=0, y=lower_height)

        # Calculate the extension line A termination point
        offset_a_x =  self.thickness * np.sin(self.ac_rad)
        offset_a_y = -self.thickness * np.cos(self.ac_rad)
        self.extension_a = deepcopy(self.lower_spiral_a).offset_by_xyz(x=offset_a_x, y=offset_a_y)

        # Calculate the extension line B termination point
        offset_b_x =  self.thickness * np.sin(self.bc_rad)
        offset_b_y = -self.thickness * np.cos(self.bc_rad)
        self.extension_b = deepcopy(self.lower_spiral_b).offset_by_xyz(x=offset_b_x, y=offset_b_y)

        # Calculate the start (point A) of the upper spiral
        neighbour_a = deepcopy(self.lower_spiral_a).offset_by_xyz(x=self.horizontal_pitch, y=self.vertical_pitch)
        extension_a_slope = np.tan(self.ac_rad)
        neighbour_a_slope = np.tan(self.ac_rad - np.pi / 2)
        self.upper_spiral_a = find_intercept(self.extension_a, extension_a_slope, neighbour_a, neighbour_a_slope)

        # Calculate the end (point B) of the upper spiral
        neighbour_b = deepcopy(self.lower_spiral_b).offset_by_xyz(x=self.horizontal_pitch, y=self.vertical_pitch)
        extension_b_slope = np.tan(self.bc_rad)
        neighbour_b_slope = np.tan(self.bc_rad - np.pi / 2)
        self.upper_spiral_b = find_intercept(self.extension_b, extension_b_slope, neighbour_b, neighbour_b_slope)


    def check_extension_orientation(self):
        """Check the orientation of the extensions at adjust if necessary."""

        # Check if the extension goes from top right to left right (x=-1, y=-1)
        ext_a_chord_line = Line(start=self.extension_a, end=self.upper_spiral_a)
        if ext_a_chord_line.get_orientation() == (1, -1):
            print('WARNING: Perpendicularity is clashing with upper spiral geometry. Adjusting termination point A')
            offset_a_x = self.chord_lower / 100 * np.cos(self.ac_rad)
            offset_a_y = self.chord_lower / 100 * np.sin(self.ac_rad)
            self.upper_spiral_a = deepcopy(self.extension_a).offset_by_xyz(x=offset_a_x, y=offset_a_y)

        # Check if the extension goes from top left to bottom right (x=1, y=-1)
        ext_b_chord_line = Line(start=self.upper_spiral_b, end=self.extension_b)
        if ext_b_chord_line.get_orientation() == (1, -1):
            print('WARNING: Perpendicularity is clashing with upper spiral geometry. Adjusting termination point B')
            offset_b_x = -self.chord_lower / 100 * np.cos(self.bc_rad)
            offset_b_y = -self.chord_lower / 100 * np.sin(self.bc_rad)
            self.upper_spiral_b = deepcopy(self.extension_b).offset_by_xyz(x=offset_b_x, y=offset_b_y)


    def calculate_poly_lines_for_spirals(self, num_points=400):
        """Generates a PolyLine representing the logarithmic spirals"""

        upper_str, lower_str = 'upper_spiral', 'lower_spiral'
        spiral_attributes = [(self.upper_spiral_a, self.upper_spiral_b, upper_str, num_points),
                             (self.lower_spiral_a, self.lower_spiral_b, lower_str, num_points + 2)]

        for start, end, label, n_points in spiral_attributes:
            a_xy, b_xy = (start.x, start.y), (end.x, end.y)
            spiral = LogarithmicSpiral(a_xy, b_xy, self.ac_deg, self.bc_deg, name=label)
            spiral.calculate_origin_offsets(self.horizontal_pitch, self.vertical_pitch, self.thickness)
            xx, yy = spiral.generate_spiral_coordinates(num_points=n_points)
            xx, yy = xx.tolist(), yy.tolist()
            if label == upper_str:
                self.pl_upper_spiral = PolyLine.generate_from_lists_of_floats(xx, yy, label=label)
            else: # Reverse the direction of the coordinates to ensure orientation remains CCW
                xx.reverse()
                yy.reverse()
                self.pl_lower_spiral = PolyLine.generate_from_lists_of_floats(xx, yy, label=label)


    def calculate_poly_lines_for_extensions(self):
        """Generates PolyLines representing the straight extensions to the upper logarithmic spiral"""
        self.pl_extension_a = PolyLine.generate_from_coordinate_list(
            [self.extension_a, self.upper_spiral_a], label='extension_a')
        self.pl_extension_b = PolyLine.generate_from_coordinate_list(
            [self.upper_spiral_b, self.extension_b], label='extension_b')


    def calculate_fillets_and_end_points(self):
        """Generates PolyLines for fillets and coordinates for end points"""

        str_a, str_b = 'fillet_a', 'fillet_b'
        fillet_attributes = [(self.extension_b, self.lower_spiral_b, str_b),
                             (self.lower_spiral_a, self.extension_a, str_a)]
        for start, end, label in fillet_attributes:
            xx, yy = PolyLine.generate_semi_circle_from_coordinates(start, end)
            mid_x, mid_y = xx[len(xx) // 2], yy[len(yy) // 2]
            if label == str_a:
                self.pl_fillet_a = PolyLine.generate_from_lists_of_floats(xx, yy, label=label)
                self.end_point_a = Coordinate(mid_x, mid_y)

            else:
                self.pl_fillet_b = PolyLine.generate_from_lists_of_floats(xx, yy, label=label)
                self.end_point_b = Coordinate(mid_x, mid_y)


    def calculate_poly_outline(self):
        """Creates a PolyLine that describes the outer perimeter of the logarithmic vane"""
        # PolyLines in counter-clockwise order starting from the centre of fillet a
        a_centre = len(self.pl_fillet_a) // 2
        self.pl_outline = PolyLine(label='vane')
        self.pl_outline += self.pl_fillet_a[a_centre:-1]
        self.pl_outline += self.pl_extension_a[:-1]
        self.pl_outline += self.pl_upper_spiral[:-1]
        self.pl_outline += self.pl_extension_b[:-1]
        self.pl_outline += self.pl_fillet_b[:-1]
        self.pl_outline += self.pl_lower_spiral[:-1]
        self.pl_outline += self.pl_fillet_a[0:a_centre + 1]


    def calculate_gap(self):
        """Calculates the diagonal gap between the vanes"""
        if self.gap is None:
            if self.horizontal_pitch is None or self.vertical_pitch is None:
                raise ValueError('horizontal_pitch and vertical_pitch cannot be None')
            self.gap = (self.horizontal_pitch ** 2 + self.vertical_pitch ** 2) ** 0.5
        return self.gap


    def calculate_pitch_angle(self):
        """Calculates the angle of the pitch line to the horizontal axis"""
        if self.horizontal_pitch is None or self.vertical_pitch is None:
            raise ValueError('horizontal_pitch and vertical_pitch cannot be None')
        return np.arctan2(self.vertical_pitch, self.horizontal_pitch)


    def offset_by_xyz(self, x:float=None, y:float=None, z:float=None):
        # Offsets the location of the vane by a specified x, y, and z component
        for poly_line in self.get_all_poly_lines():
            poly_line.offset_by_xyz(x=x, y=y, z=z)
        for coordinate in self.get_all_coordinates():
            coordinate.offset_by_xyz(x=x, y=y, z=z)


    def plot(self):
        """Plot the vane on a standard cartesian plane"""
        xx, yy = self.pl_outline.xx, self.pl_outline.yy
        plt.plot(xx, yy, label=self.pl_outline.label)
        title = (f"Angle = {self.bc_deg - self.ac_deg}  Chord = {self.chord_lower}  Stretch = {self.stretch_lower}\n"
                 f"Vertical Pitch = {self.vertical_pitch}  Horizontal Pitch = {self.horizontal_pitch}")
        min_lim = -self.thickness * 2
        max_lim = self.chord_lower
        plot_graph_elements(title=title, min_x=min_lim, min_y=min_lim, max_x=max_lim, max_y=max_lim)


    def plot_with_gradient(self):
        xx, yy = self.pl_outline.xx, self.pl_outline.yy
        points = np.array([xx, yy]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)

        # Gradient from blue to red
        cmap = LinearSegmentedColormap.from_list("blue_red", ["blue", "red"])
        norm = plt.Normalize(0, len(segments))
        lc = LineCollection(segments, cmap=cmap, norm=norm)
        lc.set_array(np.arange(len(segments)))
        lc.set_linewidth(2)

        fig, ax = plt.subplots()
        ax.add_collection(lc)
        ax.autoscale()
        ax.set_aspect('equal', 'box')

        title = (f"Angle = {self.bc_deg - self.ac_deg}  Chord = {self.chord_lower}  Stretch = {self.stretch_lower}\n"
                 f"Vertical Pitch = {self.vertical_pitch}  Horizontal Pitch = {self.horizontal_pitch}")
        min_lim = -self.thickness * 2
        max_lim = self.chord_lower
        plot_graph_elements(title=title, min_x=min_lim, min_y=min_lim, max_x=max_lim, max_y=max_lim)

        plt.show()


    def plot_components(self, file_directory:None):
        poly_lines = [
            self.pl_extension_a,
            self.pl_upper_spiral,
            self.pl_extension_b,
            self.pl_fillet_b,
            self.pl_lower_spiral,
            self.pl_fillet_a]
        for poly_line in poly_lines:
            xx, yy = poly_line.xx, poly_line.yy
            plt.plot(xx, yy, label=poly_line.label)

        file_name = (f"angle_{self.bc_deg - self.ac_deg}_"
                     f"chord_{self.chord_lower}_"
                     f"stretch_{self.stretch_lower:.2f}_"
                     f"v_pitch_{self.vertical_pitch:.2f}_"
                     f"h_pitch_{self.horizontal_pitch:.2f}")
        file_name = file_name.replace('.', '-')

        title = (f"Angle = {self.bc_deg - self.ac_deg}  Chord = {self.chord_lower}  Stretch = {self.stretch_lower}\n"
                 f"Vertical Pitch = {self.vertical_pitch}  Horizontal Pitch = {self.horizontal_pitch}")


        min_lim = -self.thickness * 2
        max_lim = self.chord_lower
        plot_graph_elements(title=title, min_x=min_lim, min_y=min_lim, max_x=max_lim, max_y=max_lim,
                            file_name=file_name, file_directory=file_directory)


    # ------ Methods to generate Vane Cascades ----------------------------------------------------------------------- #

    def save_cascade_characteristics(self, stl_scale, file_directory):
        """Saves the most important cascade characteristics to a .text file"""
        # Scale the values according to the input scale
        horizontal_pitch = self.horizontal_pitch * stl_scale
        vertical_pitch = self.vertical_pitch * stl_scale
        chord = self.chord_lower * stl_scale
        # Create the overview file
        with open(f"{file_directory}/_cascade_characteristics.txt", "w") as f:
            # Write file header
            f.write(f'The characteristics for the simulated vane cascade are as follows:\n')
            f.write(f'Horizontal pitch:     {horizontal_pitch}\n')
            f.write(f'Vertical pitch:       {vertical_pitch}\n')
            f.write(f'Gap:                  {(horizontal_pitch ** 2 + vertical_pitch ** 2) ** 0.5}\n')
            f.write(f'Chord:                {chord}\n')
            f.write(f'Stretch:              {self.stretch_lower}\n')
            f.write(f'Separation (x y z):   {horizontal_pitch} {vertical_pitch} 0\n')


    def calculate_mid_points(self,
                             end_lower:Coordinate,
                             end_upper:Coordinate,
                             extension_angle:float,
                             num_gaps:int) -> tuple[Coordinate, Coordinate]:
        """Calculate the lower-mid and upper-mid channel points"""
        projected_angle = extension_angle - (np.pi / 2)
        pitch_angle = self.calculate_pitch_angle()
        offset_angle = projected_angle - pitch_angle
        diagonal_pitch = self.gap
        projected_distance = np.cos(offset_angle) * (diagonal_pitch * num_gaps / 3)
        x_offset = projected_distance * np.cos(projected_angle)
        y_offset = projected_distance * np.sin(projected_angle)
        end_lower_mid = deepcopy(end_lower)
        end_lower_mid.offset_by_xyz(x_offset, y_offset)
        end_upper_mid = deepcopy(end_upper)
        end_upper_mid.offset_by_xyz(-x_offset, -y_offset)
        return end_lower_mid, end_upper_mid


    def calculate_end_points(self,
                             vane_end_lower: Coordinate,
                             channel_length: float,
                             extension_angle: float,
                             orientation: int,
                             num_gaps: int) -> tuple[Coordinate, Coordinate]:
        """Calculates the lower and upper channel midpoints"""
        # Calculate the lower channel point
        channel_start_x = vane_end_lower.x + orientation * channel_length * np.cos(extension_angle)
        channel_start_y = vane_end_lower.y + orientation * channel_length * np.sin(extension_angle)
        end_lower = Coordinate(channel_start_x, channel_start_y)
        # Calculate the upper channel point
        x_offset, y_offset = self.horizontal_pitch * num_gaps, self.vertical_pitch * num_gaps
        end_upper = deepcopy(end_lower).offset_by_xyz(x_offset, y_offset)
        return end_lower, end_upper


    def get_end_lower_and_upper_poly_lines(
            self,
            vane_end_lower: Coordinate,
            vane_end_upper: Coordinate,
            channel_length: float,
            extension_angle: float,
            orientation: int,
            num_gaps: int,
            location: str,
            location_b_str: str,
            end_label: str):

        # Calculate the various end points
        end_lower, end_upper = self.calculate_end_points(vane_end_lower, channel_length, extension_angle, orientation, num_gaps)
        end_lower_mid, end_upper_mid = self.calculate_mid_points(end_lower, end_upper, extension_angle, num_gaps)

        # Define the wall and end coordinates anti-clockwise around the vane domain
        lower_coordinates = [end_lower, vane_end_lower]
        upper_coordinates = [vane_end_upper, end_upper]
        end_coordinates = [end_lower, end_lower_mid, end_upper_mid, end_upper]
        if location == location_b_str:
            end_coordinates.reverse()

        # Generate PolyLines from the list of coordinates
        lower_poly_line = PolyLine.generate_from_coordinate_list(lower_coordinates, label=f'patch_{location}_lower')
        upper_poly_line = PolyLine.generate_from_coordinate_list(upper_coordinates, label=f'patch_{location}_upper')
        end_poly_line = PolyLine.generate_from_coordinate_list(end_coordinates, label=end_label)

        return end_poly_line, lower_poly_line, upper_poly_line


    def get_vane_and_refinement_poly_lines(self, num_vanes:int) -> tuple[list[PolyLine], list[PolyLine], list[PolyLine]]:
        """Calculates the vane and refinement surfaces to an .stl file"""
        vanes, refine_a, refine_b = list(), list(), list()
        for i in range(num_vanes):
            x_offset, y_offset = i * self.horizontal_pitch, i * self.vertical_pitch
            vanes.append(deepcopy(self.pl_outline).offset_by_xyz(x=x_offset, y=y_offset))
            refine_a.append(deepcopy(self.pl_fillet_a).offset_by_xyz(x=x_offset, y=y_offset))
            refine_b.append(deepcopy(self.pl_fillet_b).offset_by_xyz(x=x_offset, y=y_offset))
        return vanes, refine_a, refine_b


    def generate_cascade(
            self,
            upstream_channel_length: float,
            downstream_channel_length: float,
            num_vanes=2,
            file_directory=None,
            stl_height=1,
            stl_scale=1,
            show_plot=False,
            show_channel=False):

        """Generates a cascade of expansion vanes from a single logarithmic expansion vane"""
        print('\nGenerating a expansion vane cascade from a singe logarithmic vane')

        if num_vanes < 2:
            print('Minimum number of vanes must be at least 2. Setting number of vanes to 2')
            num_vanes = 2

        # Create stable iterable for the vane ends
        location_a_str, location_b_str = 'a', 'b'
        lower_vane_ends = [(self.end_point_a, location_a_str), (self.end_point_b, location_b_str)]

        channel_walls, channel_ends = list(), list()
        for vane_end_lower, location in lower_vane_ends:

            # Calculate the upper vane end
            num_gaps = num_vanes - 1
            x_offset, y_offset = self.horizontal_pitch * num_gaps, self.vertical_pitch * num_gaps
            vane_end_upper = deepcopy(vane_end_lower).offset_by_xyz(x=x_offset, y=y_offset)

            if location == location_a_str:
                orientation = -1
                extension_angle = self.ac_rad
                end_label = 'inlet'
                channel_length = upstream_channel_length
            else:
                orientation = 1
                extension_angle = self.bc_rad
                end_label = 'outlet'
                channel_length = downstream_channel_length

            end_poly_line, lower_poly_line, upper_poly_line = self.get_end_lower_and_upper_poly_lines(
                vane_end_lower,
                vane_end_upper,
                channel_length,
                extension_angle,
                orientation, num_gaps,
                location,
                location_b_str,
                end_label)

            # Group the channel walls and ends into the relevant list
            channel_ends.append(end_poly_line)
            channel_walls.append(lower_poly_line)
            channel_walls.append(upper_poly_line)

        # Generate vane and refinement surfaces
        vanes, refine_a, refine_b = self.get_vane_and_refinement_poly_lines(num_vanes)

        if show_channel and show_plot:
            for poly_lines in [channel_walls, channel_ends]:
                for poly_line in poly_lines:
                    poly_line.plot()

        if show_plot:
            title = (
                f"Angle = {self.bc_deg - self.ac_deg}  Chord = {self.chord_lower}  Stretch = {self.stretch_lower}\n"
                f"Vertical Pitch = {self.vertical_pitch}  Horizontal Pitch = {self.horizontal_pitch}")
            for poly_lines in [vanes]:
                for poly_line in poly_lines:
                    poly_line.plot()
            plot_graph_elements(title=title)

        print('Creating PolyLines for chanel walls and channel ends')
        for poly_lines in [channel_walls, channel_ends]:
            for poly_line in poly_lines:
                PolyLine.create_stl_file_from_xy_poly_line(
                    poly_lines=poly_line,
                    height=stl_height,
                    file_directory=file_directory,
                    stl_scale=stl_scale)

        print('Creating PolyLines for refinement surfaces')
        for poly_lines, name in [(refine_a, 'tip_refinements_a'), (refine_b, 'tip_refinements_b')]:
            PolyLine.create_stl_file_from_xy_poly_line(
                poly_lines=poly_lines,
                height=stl_height,
                file_directory=file_directory,
                stl_scale=stl_scale,
                file_name=name)

        PolyLine.create_stl_file_from_xy_poly_line(
            poly_lines=vanes,
            height=stl_height,
            create_end_cap=True,
            file_directory=file_directory,
            stl_scale=stl_scale,
            file_name='vanes')

        self.save_cascade_characteristics(stl_scale=stl_scale, file_directory=file_directory)








    def generate_cascade_2(
            self,
            upstream_channel_length: float,
            downstream_channel_length: float,
            num_vanes=2,
            file_directory=None,
            stl_height=1,
            stl_scale=1,
            show_plot=False,
            show_channel=False):

        """Generates a cascade of expansion vanes from a single logarithmic expansion vane"""
        print('\nGenerating a expansion vane cascade from a singe logarithmic vane')

        if num_vanes < 2:
            print('Minimum number of vanes must be at least 2. Setting number of vanes to 2')
            num_vanes = 2

        vanes:list[LogarithmicVane] = list()
        for vane_idx in range(num_vanes):
            vane_copy = deepcopy(self)
            vane_copy.offset_by_xyz(x=vane_idx * self.horizontal_pitch, y=vane_idx * self.vertical_pitch)
            vanes.append(vane_copy)

        # Retrieve end points
        vane_inner_end_point_a:Coordinate = vanes[0].end_point_a
        vane_inner_end_point_b:Coordinate = vanes[0].end_point_b
        vane_outer_end_point_a:Coordinate = vanes[-1].end_point_a
        vane_outer_end_point_b:Coordinate = vanes[-1].end_point_b

        # Calculate the perpendicular distance of the channel at point A
        slope_inner_a = np.tan(self.ac_rad - np.pi/2)
        slope_outer_a = np.tan(self.ac_rad)
        intercept_a = find_intercept(vane_inner_end_point_a, slope_inner_a, vane_outer_end_point_a, slope_outer_a)
        distance_a = intercept_a - vane_inner_end_point_a

        # Calculate the perpendicular distance of the channel at point B
        slope_inner_b = np.tan(self.bc_rad - np.pi/2)
        slope_outer_b = np.tan(self.bc_rad)
        intercept_b = find_intercept(vane_inner_end_point_b, slope_inner_b, vane_outer_end_point_b, slope_outer_b)
        distance_b = intercept_b - vane_inner_end_point_b

        print()







        intercept = find_intercept(vane)
        # Create stable iterable for the vane ends
        location_a_str, location_b_str = 'a', 'b'
        lower_vane_ends = [(self.end_point_a, location_a_str), (self.end_point_b, location_b_str)]

        channel_walls, channel_ends = list(), list()
        for vane_end_lower, location in lower_vane_ends:

            # Calculate the upper vane end
            num_gaps = num_vanes - 1
            x_offset, y_offset = self.horizontal_pitch * num_gaps, self.vertical_pitch * num_gaps
            vane_end_upper = deepcopy(vane_end_lower).offset_by_xyz(x=x_offset, y=y_offset)

            if location == location_a_str:
                orientation = -1
                extension_angle = self.ac_rad
                end_label = 'inlet'
                channel_length = upstream_channel_length
            else:
                orientation = 1
                extension_angle = self.bc_rad
                end_label = 'outlet'
                channel_length = downstream_channel_length

            end_poly_line, lower_poly_line, upper_poly_line = self.get_end_lower_and_upper_poly_lines(
                vane_end_lower,
                vane_end_upper,
                channel_length,
                extension_angle,
                orientation, num_gaps,
                location,
                location_b_str,
                end_label)

            # Group the channel walls and ends into the relevant list
            channel_ends.append(end_poly_line)
            channel_walls.append(lower_poly_line)
            channel_walls.append(upper_poly_line)

        # Generate vane and refinement surfaces
        vanes, refine_a, refine_b = self.get_vane_and_refinement_poly_lines(num_vanes)

        if show_channel and show_plot:
            for poly_lines in [channel_walls, channel_ends]:
                for poly_line in poly_lines:
                    poly_line.plot()

        if show_plot:
            title = (
                f"Angle = {self.bc_deg - self.ac_deg}  Chord = {self.chord_lower}  Stretch = {self.stretch_lower}\n"
                f"Vertical Pitch = {self.vertical_pitch}  Horizontal Pitch = {self.horizontal_pitch}")
            for poly_lines in [vanes]:
                for poly_line in poly_lines:
                    poly_line.plot()
            plot_graph_elements(title=title)

        print('Creating PolyLines for chanel walls and channel ends')
        for poly_lines in [channel_walls, channel_ends]:
            for poly_line in poly_lines:
                PolyLine.create_stl_file_from_xy_poly_line(
                    poly_lines=poly_line,
                    height=stl_height,
                    file_directory=file_directory,
                    stl_scale=stl_scale)

        print('Creating PolyLines for refinement surfaces')
        for poly_lines, name in [(refine_a, 'tip_refinements_a'), (refine_b, 'tip_refinements_b')]:
            PolyLine.create_stl_file_from_xy_poly_line(
                poly_lines=poly_lines,
                height=stl_height,
                file_directory=file_directory,
                stl_scale=stl_scale,
                file_name=name)

        PolyLine.create_stl_file_from_xy_poly_line(
            poly_lines=vanes,
            height=stl_height,
            create_end_cap=True,
            file_directory=file_directory,
            stl_scale=stl_scale,
            file_name='vanes')

        self.save_cascade_characteristics(stl_scale=stl_scale, file_directory=file_directory)


