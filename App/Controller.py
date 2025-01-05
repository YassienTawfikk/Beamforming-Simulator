from PyQt5 import QtWidgets, QtGui

import math
import numpy as np
import pyqtgraph as pg

from App.UI.Design import Ui_MainWindow
from App.Logging_Manager import LoggingManager
from App.Simulation import BeamformingSimulator


class MainController:
    def __init__(self, app):
        self.app = app
        self.main_window = QtWidgets.QMainWindow()

        self.view = Ui_MainWindow()
        self.logging = LoggingManager()

        self.initialize_view()
        self.initialize_arrays_info()

    def initialize_view(self):
        self.view.setupUi(self.main_window)
        self.view.scenarios_button.clicked.connect(self.toggle_scenario)
        self.current_scenario = None

        self.view.arrays_number_SpinBox.editingFinished.connect(self.update_current_arrays_number)
        self.view.elements_number_SpinBox.editingFinished.connect(self.update_current_elements_number)

        self.view.elements_spacing_slider.valueChanged.connect(self.update_elements_space_label)
        self.view.elements_spacing_slider.valueChanged.connect(self.update_elements_spacing)

        self.view.array_curve_slider.valueChanged.connect(self.update_elements_curvature_label)
        self.view.array_curve_slider.sliderReleased.connect(self.update_elements_curvature)

        self.view.steering_angle_slider.valueChanged.connect(self.update_steering_label)
        self.view.steering_angle_slider.valueChanged.connect(self.update_steering_angle)

        self.view.operating_frequency_spinbox.valueChanged.connect(self.update_operating_frequency)
        self.view.operating_frequency_range_combobox.currentIndexChanged.connect(self.update_spacing_frequency)

        self.view.quit_app_button.clicked.connect(self.close_application)

    def toggle_scenario(self):
        scenario_settings = {
            '5G': {
                'frequency': 30,
                'frequency_bandwidth_index': 2,
                'elements_spacing': 50,
                'curvature': 0,
                'num_elements': 32
            },
            'Ultrasound': {
                'frequency': 100,
                'frequency_bandwidth_index': 2,
                'elements_spacing': 10,
                'curvature': 90,
                'num_elements': 64
            },
            'Tumor Ablation': {
                'frequency': 50,
                'frequency_bandwidth_index': 2,
                'elements_spacing': 15,
                'curvature': 0,
                'num_elements': 128
            }
        }

        scenarios = list(scenario_settings.keys())
        if self.current_scenario is None:
            self.current_scenario = '5G'
        else:
            current_index = scenarios.index(self.current_scenario)
            self.current_scenario = scenarios[(current_index + 1) % len(scenarios)]

        self.logging.log(f"Switching scenario to {self.current_scenario}")

        scenario = scenario_settings[self.current_scenario]

        # Update operating frequency
        self.view.operating_frequency_spinbox.setValue(scenario['frequency'])
        self.view.operating_frequency_range_combobox.setCurrentIndex(scenario['frequency_bandwidth_index'])
        self.update_operating_frequency()

        # Update array settings
        self.view.elements_spacing_slider.setValue(scenario['elements_spacing'])
        self.update_elements_spacing()

        self.view.array_curve_slider.setValue(scenario['curvature'])
        self.update_elements_curvature()

        self.view.elements_number_SpinBox.setValue(scenario['num_elements'])
        self.update_current_elements_number()

        # Log the updated settings
        self.logging.log(
            f"""
            Updated to scenario: {self.current_scenario}
            Operating Frequency: {self.view.format_frequency(self.view.current_operating_frequency)},
            Element Spacing: {self.view.current_elements_spacing} m,
            Curvature: {self.view.current_array_curvature_angle} degrees,
            Number of Elements: {scenario['num_elements']}
            """
        )

        # Update UI and arrays
        self.view.scenarios_button.setText(self.current_scenario)
        self.view.updateVisualization()
        self.update_and_refresh_arrays_info()

    def initialize_arrays_info(self):
        # Start with an empty list of configurations
        self.configurations = []

        # Retrieve the configuration for each array
        spacing, num_elements, curvature = self.view.visualization_widget.get_array_configuration(1)
        # Append a new dictionary to the configurations list with the retrieved settings
        self.configurations.append({
            'num_elements': num_elements,
            'spacing': spacing,
            'curvature': curvature
        })
        self.model = BeamformingSimulator(self.view.current_operating_frequency, self.view.current_steering_angle, self.configurations)
        self.array_visualize(num_elements, spacing, curvature)
        self.apply_configurations_to_visualization()

    def array_visualize(self, num_elements, spacing, curvature_degrees):
        curvature_degrees = max(0, min(curvature_degrees, 180))
        a = curvature_degrees / 10.0
        center_index = (num_elements - 1) / 2.0
        x_coords = [(i - center_index) * spacing for i in range(num_elements)]
        y_coords = [a * (x ** 2) for x in x_coords]
        self.view.arrayShapeItem.clear()
        self.view.arrayShapeItem.plot(
            x_coords,
            y_coords,
            pen=None,
            symbol='o',
            symbolSize=10,
            symbolBrush='w'
        )
        x_min, x_max = min(x_coords), max(x_coords)
        y_min, y_max = min(y_coords), max(y_coords)
        x_padding = spacing * 0.5
        y_range = y_max - y_min
        y_padding = y_range * 0.5 if y_range > 0 else 1
        self.view.arrayShapeItem.setXRange(x_min - x_padding, x_max + x_padding, padding=0)
        self.view.arrayShapeItem.setYRange(y_min - y_padding, y_max + y_padding, padding=0)
        self.view.arrayShapeItem.showGrid(x=True, y=True, alpha=0.3)

    def update_and_refresh_arrays_info(self):
        # Clear the existing configurations to ensure no outdated data is kept
        self.configurations.clear()

        # Reinitialize the configurations by fetching current settings from the visualization widget
        for i in range(1, self.view.current_arrays_number + 1):
            try:
                # Retrieve the configuration for each array
                spacing, num_elements, curvature = self.view.visualization_widget.get_array_configuration(i)
                # Append a new dictionary to the configurations list with the retrieved settings
                self.configurations.append({
                    'num_elements': num_elements,
                    'spacing': spacing,
                    'curvature': curvature
                })
            except IndexError:
                # Handle cases where the index is out of range, potentially logging or adding default configurations
                self.logging.log(f"Failed to retrieve configuration for array {i}, using default settings.")
                self.configurations.append({
                    'num_elements': 64,  # Default value if out of range
                    'spacing': 0.05,  # Default value if out of range
                    'curvature': 0  # Default value if out of range
                })
        spacing, num_elements, curvature = self.view.visualization_widget.get_array_configuration(1)
        self.array_visualize(num_elements, self.view.elements_spacing_slider.value(), curvature)

        # Optionally update visualization widget here if necessary
        self.apply_configurations_to_visualization()

    def apply_configurations_to_visualization(self):
        # Assuming self.model is an instance of BeamformingSimulator
        x_range = (-10, 10)
        y_range = (0, 10)
        x, y, intensity = self.model.simulate_multiple_arrays(x_range, y_range)

        angles = np.linspace(-90, 90, 500)  # Angles to compute beam profile (in degrees)
        array_factor = self.model.calculate_array_factor(angles)

        # Clear previous plots
        self.view.intensityImageItem.clear()
        self.view.beamProfileLine.clear()

        # Plot intensity heatmap on the intensityMapItem
        self.view.intensityImageItem.setImage(intensity.T)  # Transpose intensity for correct orientation
        self.view.intensityImageItem.setLevels([np.min(intensity), np.max(intensity)])  # Color scaling
        self.view.intensityMapItem.getViewBox().setRange(
            xRange=(0, 200),
            yRange=(0, 200),
            padding=0
        )
        self.view.intensityMapItem.setTitle("Intensity Map")
        self.view.intensityMapItem.getAxis('left').setLabel("Y-axis")
        self.view.intensityMapItem.getAxis('bottom').setLabel("X-axis")

        # Plot beam profile on the beamProfileItem
        self.view.beamProfileLine.setData(angles, array_factor)
        self.view.beamProfileItem.setTitle("Beam Profile")
        self.view.beamProfileItem.getAxis('left').setLabel("Array Factor")
        self.view.beamProfileItem.getAxis('bottom').setLabel("Angle (°)")

    # --------------------------------------------------------------------------------------------------------------------------------------

    def update_current_arrays_number(self):
        self.view.current_arrays_number = self.view.arrays_number_SpinBox.value()
        self.view.arrays_parameters_indicator.setText(f"{self.view.current_arrays_number} Arrays")
        self.view.current_selected_array = 0
        self.view.current_selected_ALL_array = True
        self.view.current_selected_array_button.setText("All Arrays")
        self.view.visualization_widget.updateArrayNumber(self.view.current_arrays_number)

    def update_current_elements_number(self):
        self.view.current_elements_number = self.view.elements_number_SpinBox.value()
        self.view.arrays_parameters_indicator.setText(f"{self.view.current_elements_number} Elements")
        self.view.updateVisualization()
        self.update_and_refresh_arrays_info()

    def update_elements_space_label(self):
        self.view.arrays_parameters_indicator.setText(f"{self.view.elements_spacing_slider.value()}% Wavelength")

    def update_elements_spacing(self):
        if self.view.current_operating_frequency > 0:
            self.view.current_elements_spacing = (self.view.elements_spacing_slider.value() / 100) * self.model.wavelength
        else:
            self.view.current_elements_spacing = 0  # or some default value, or raise an error/message to the user
        self.view.updateVisualization()
        self.update_and_refresh_arrays_info()

    def update_elements_curvature_label(self):
        self.view.arrays_parameters_indicator.setText(f"{self.view.array_curve_slider.value()} Degree")

    def update_elements_curvature(self):
        self.view.current_array_curvature_angle = self.view.array_curve_slider.value()
        self.update_elements_curvature_label()
        self.view.updateVisualization()
        self.update_and_refresh_arrays_info()

    def update_steering_angle(self):
        self.view.current_steering_angle = self.view.steering_angle_slider.value()
        self.model.update_steering_angle(self.view.current_steering_angle)
        self.apply_configurations_to_visualization()

    def update_steering_label(self):
        self.view.sidebar_parameter_indicator.setText(f"{self.view.steering_angle_slider.value()} Degree")

    def update_operating_frequency(self):
        index = self.view.operating_frequency_range_combobox.currentIndex()
        range = 10 ** (3 * (index + 1))
        self.view.current_operating_frequency = self.view.operating_frequency_spinbox.value() * range
        formatted_frequency = self.view.format_frequency(self.view.current_operating_frequency)
        self.view.sidebar_parameter_indicator.setText(formatted_frequency)
        self.model.update_operating_frequency(self.view.current_operating_frequency)
        # self.update_elements_spacing()
        self.apply_configurations_to_visualization()

    def update_spacing_frequency(self):
        index = self.view.operating_frequency_range_combobox.currentIndex()
        range = 10 ** (3 * (index + 1))
        self.view.current_operating_frequency = self.view.operating_frequency_spinbox.value() * range
        formatted_frequency = self.view.format_frequency(self.view.current_operating_frequency)
        self.view.sidebar_parameter_indicator.setText(formatted_frequency)
        self.model.update_operating_frequency(self.view.current_operating_frequency)
        self.update_elements_spacing()
        self.apply_configurations_to_visualization()

    # --------------------------------------------------------------------------------------------------------------------------------------
    def close_application(self):
        self.logging.log(f"Application Closed")
        self.main_window.close()

    def run(self):
        self.logging.log("Application Opened")
        self.main_window.showFullScreen()
        return self.app.exec_()
