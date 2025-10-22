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


    def calculate_poly_lines_for_spirals(self, num_points=90):
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

    def save_cascade_characteristics(self, num_vanes:int, stl_scale: float, file_directory:str, measure_a:Line, measure_b:Line):
        """Saves the most important cascade characteristics to a .text file"""
        # Scale the values according to the input scale
        horizontal_pitch = self.horizontal_pitch * stl_scale
        vertical_pitch = self.vertical_pitch * stl_scale
        chord = self.chord_lower * stl_scale
        num_gaps = num_vanes - 1
        # Create the overview file
        with open(f"{file_directory}/_cascade_characteristics.txt", "w") as f:
            # Write file header
            f.write(f'The characteristics for the simulated vane cascade are as follows:\n')
            f.write(f'Horizontal pitch:  {horizontal_pitch}\n')
            f.write(f'Vertical pitch:    {vertical_pitch}\n')
            f.write(f'Gap:               {(horizontal_pitch ** 2 + vertical_pitch ** 2) ** 0.5}\n')
            f.write(f'Chord:             {chord}\n')
            f.write(f'Stretch:           {self.stretch_lower}\n\n')
            f.write(f'Number of vanes:   {num_vanes}\n\n')
            f.write(f'Settings for the CFD simulation:\n')
            f.write(f'Separation (x y z):        ({horizontal_pitch * num_gaps} {vertical_pitch * num_gaps } 0)\n')
            f.write(f'Measure upstream start:    ({measure_a.start.x} {measure_a.start.x} 0)\n')
            f.write(f'Measure upstream end:      ({measure_a.end.x} {measure_a.end.x} 0)\n')
            f.write(f'Measure downstream start:  ({measure_b.start.x} {measure_b.start.x} 0)\n')
            f.write(f'Measure downstream end:    ({measure_b.end.x} {measure_b.end.x} 0)\n')


    @staticmethod
    def get_channel_width(inner_endpoint, outer_endpoint, angle):
        # Calculate the perpendicular distance of the channel at point A
        slope_inner, slope_outer = np.tan(angle - np.pi / 2), np.tan(angle)
        intercept = find_intercept(inner_endpoint, slope_inner, outer_endpoint, slope_outer)
        width_xyz = intercept - inner_endpoint
        channel_width = sum([i ** 2 for i in width_xyz]) ** 0.5
        return channel_width


    def generate_cascade(
            self,
            upstream_channel_len: float,
            downstream_channel_len: float,
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
        refine_a:list[PolyLine] = list()
        refine_b:list[PolyLine] = list()
        for i in range(num_vanes):
            x_offset, y_offset = i * self.horizontal_pitch, i * self.vertical_pitch
            vane_copy = deepcopy(self)
            vane_copy.offset_by_xyz(x=x_offset, y=y_offset)
            vanes.append(vane_copy)
            refine_a.append(vane_copy.pl_fillet_a)
            refine_b.append(vane_copy.pl_fillet_b)

        # Retrieve vane end points
        vane_end_inner_a:Coordinate = vanes[0].end_point_a
        vane_end_inner_b:Coordinate = vanes[0].end_point_b
        vane_end_outer_a:Coordinate = vanes[-1].end_point_a
        vane_end_outer_b:Coordinate = vanes[-1].end_point_b

        # Calculate channel end points
        end_inner_a = deepcopy(vane_end_inner_a).offset_by_dist_and_angle(upstream_channel_len, -self.ac_rad)
        end_outer_a = deepcopy(vane_end_outer_a).offset_by_dist_and_angle(upstream_channel_len, -self.ac_rad)
        end_inner_b = deepcopy(vane_end_inner_b).offset_by_dist_and_angle(downstream_channel_len, self.bc_rad)
        end_outer_b = deepcopy(vane_end_outer_b).offset_by_dist_and_angle(downstream_channel_len, self.bc_rad)

        # Calculate channel measurement points
        offset_a = 200
        measure_inner_a = deepcopy(vane_end_inner_a).offset_by_dist_and_angle(offset_a, -self.ac_rad)
        measure_outer_a = deepcopy(vane_end_outer_a).offset_by_dist_and_angle(offset_a, -self.ac_rad)
        measure_a = Line(start=measure_inner_a, end=measure_outer_a)
        offset_b = 200
        measure_inner_b = deepcopy(vane_end_inner_b).offset_by_dist_and_angle(offset_b, self.bc_rad)
        measure_outer_b = deepcopy(vane_end_outer_b).offset_by_dist_and_angle(offset_b, self.bc_rad)
        measure_b = Line(start=measure_inner_b, end=measure_outer_b)


        # Calculate channel end mid points
        w_a = self.get_channel_width(vane_end_inner_a, vane_end_outer_a, self.ac_rad)
        end_inner_mid_a = deepcopy(end_inner_a).offset_by_dist_and_angle(w_a / 3, self.ac_rad - np.pi / 2)
        end_outer_mid_a = deepcopy(end_outer_a).offset_by_dist_and_angle(w_a / 3, self.ac_rad + np.pi / 2)
        w_b = self.get_channel_width(vane_end_inner_b, vane_end_outer_b, self.bc_rad) / 3
        end_inner_mid_b = deepcopy(end_inner_b).offset_by_dist_and_angle(w_b / 3, self.bc_rad - np.pi / 2)
        end_outer_mid_b = deepcopy(end_outer_b).offset_by_dist_and_angle(w_b / 3, self.bc_rad + np.pi / 2)

        # Define channel side walls (in anti-clockwise order)
        side_outer_a = PolyLine.generate_from_coordinate_list([end_outer_a, vane_end_outer_a], 'patch_a_outer')
        side_outer_b = PolyLine.generate_from_coordinate_list([vane_end_outer_b, end_outer_b], 'patch_b_outer')
        side_inner_b = PolyLine.generate_from_coordinate_list([end_inner_b, vane_end_inner_b], 'patch_b_inner')
        side_inner_a = PolyLine.generate_from_coordinate_list([vane_end_inner_a, end_inner_a], 'patch_a_inner')

        # Define channel end walls (in anti-clockwise order)
        coordinates_a = [end_inner_a, end_inner_mid_a, end_outer_mid_a, end_outer_a]
        end_a = PolyLine.generate_from_coordinate_list(coordinates_a, 'inlet')
        coordinates_b = [end_outer_b, end_outer_mid_b, end_inner_mid_b, end_inner_b]
        end_b = PolyLine.generate_from_coordinate_list(coordinates_b, 'outlet')

        # Plot the vane cascade and the generated channel
        if show_plot:
            for vane in vanes:
                vane.pl_outline.plot()
            if show_channel:
                for poly_line in [side_outer_a, side_outer_b, end_b, side_inner_b, side_inner_a, end_a]:
                    poly_line.plot()
            title = (
                f"Angle = {self.bc_deg - self.ac_deg}  Chord = {self.chord_lower}  Stretch = {self.stretch_lower}\n"
                f"Vertical Pitch = {self.vertical_pitch}  Horizontal Pitch = {self.horizontal_pitch}")
            plot_graph_elements(title=title)

        # Create STL files for the channel sides and ends
        print('Creating PolyLines for the chanel walls and channel ends')
        for poly_line in [side_outer_a, side_outer_b, side_inner_b, side_inner_a, end_a, end_b]:
            PolyLine.create_stl_file_from_xy_poly_line(
                poly_lines=poly_line,
                height=stl_height,
                file_directory=file_directory,
                stl_scale=stl_scale)

        # Create STL files for the refinement surfaces
        print('Creating PolyLines for the refinement surfaces')
        for poly_lines, name in [(refine_a, 'tip_refinements_a'), (refine_b, 'tip_refinements_b')]:
            PolyLine.create_stl_file_from_xy_poly_line(
                poly_lines=poly_lines,
                height=stl_height,
                file_directory=file_directory,
                stl_scale=stl_scale,
                file_name=name)

        # Create an STL file for the turning vnaes
        print('Creating PolyLines for the vanes')
        pl_vanes = [vane.pl_outline for vane in vanes if vane.pl_outline]
        PolyLine.create_stl_file_from_xy_poly_line(
            poly_lines=pl_vanes,
            height=stl_height,
            create_end_cap=True,
            file_directory=file_directory,
            stl_scale=stl_scale,
            file_name='vanes')

        # Save the characteristics of the vane cascade
        self.save_cascade_characteristics(num_vanes=num_vanes, stl_scale=stl_scale, file_directory=file_directory,
                                          measure_a=measure_a, measure_b=measure_b)



