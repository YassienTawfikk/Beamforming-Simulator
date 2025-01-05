import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from math import sin, radians


class BeamformingSimulator:
    def __init__(self, frequency, steering_angle, arrays_info):
        self.frequency = frequency  # Operating frequency in Hz
        self.steering_angle = steering_angle  # Steering angle in degrees
        self.arrays_info = arrays_info  # Store array configurations
        self.wavelength = 3e8 / self.frequency  # Calculate wavelength from frequency
        self.k = 2 * np.pi / self.wavelength  # Calculate wave number

    def simulate_multiple_arrays(self, x_range, y_range):
        """
        Simulate multiple arrays with given configurations and return intensity map.

        Args:
            x_range (tuple): Range of x-coordinates (min, max).
            y_range (tuple): Range of y-coordinates (min, max).

        Returns:
            x (numpy.ndarray): x-coordinate array.
            y (numpy.ndarray): y-coordinate array.
            intensity (numpy.ndarray): Normalized intensity map.
        """
        x = np.linspace(x_range[0], x_range[1], 200)
        y = np.linspace(y_range[0], y_range[1], 200)
        X, Y = np.meshgrid(x, y)
        intensity_map = np.zeros_like(X, dtype=np.complex128)

        for array_info in self.arrays_info:
            positions = self.calculate_element_positions(array_info['num_elements'], array_info['spacing'], array_info['curvature'])
            one = -1 if array_info['curvature'] == 0 else 1
            for (ex, ey) in positions:
                distances = np.sqrt((X - ex) ** 2 + (Y - ey) ** 2)
                phase_shift = -self.k * (ex * np.sin(one * np.radians(self.steering_angle)) + ey * np.cos(np.radians(self.steering_angle)))
                intensity_map += np.exp(1j * (self.k * distances + phase_shift))

        intensity = np.abs(intensity_map) ** 2
        intensity /= np.max(intensity) + 1e-10  # Avoid division by zero
        return x, y, intensity

    def calculate_array_factor(self, angles):
        array_factor = np.zeros_like(angles, dtype=np.complex128)
        positions = self.calculate_element_positions(self.arrays_info[0]['num_elements'], self.arrays_info[0]['spacing'],
                                                     self.arrays_info[0]['curvature'])
        for x, y in positions:
            phase_shift = -self.k * (x * np.sin(np.radians(self.steering_angle)) + y * np.cos(np.radians(self.steering_angle)))
            array_factor += np.exp(1j * (self.k * (x * np.sin(np.radians(angles)) + y * np.cos(np.radians(angles))) + phase_shift))
        return np.abs(array_factor) ** 2

    def calculate_element_positions(self, num_elements, element_spacing, curvature_degree):
        positions = []
        if curvature_degree == 0:  # Linear array
            # Start at (0, 0) and lay out elements symmetrically
            positions = [(i * element_spacing - (num_elements - 1) * element_spacing / 2, 0) for i in range(num_elements)]
        else:  # Curved array
            # Calculate the radius of the arc
            arc_length = (num_elements - 1) * element_spacing
            curvature_radians = np.radians(curvature_degree)
            radius = arc_length / curvature_radians if curvature_radians != 0 else np.inf

            # Distribute elements evenly along the arc
            for i in range(num_elements):
                angle = -curvature_radians / 2 + i * (curvature_radians / (num_elements - 1))
                x = radius * np.cos(angle) - radius  # Center the arc
                y = radius * np.sin(angle)
                positions.append((x, y))

        # Debug: Print positions
        return positions

    # -------------------------------------------------------------------------------------------------------------------------------------
    def update_operating_frequency(self, frequency):
        self.frequency = frequency
        self.wavelength = 3e8 / self.frequency

        self.k = 2 * np.pi / self.wavelength

    def update_steering_angle(self, steering_angle):
        self.steering_angle = steering_angle
