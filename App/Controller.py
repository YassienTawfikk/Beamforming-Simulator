from PyQt5 import QtWidgets, QtGui
import math
import numpy as np
import pyqtgraph as pg
import os
import shutil

from app.ui.design import Ui_MainWindow
from app.logging_manager import LoggingManager
from app.simulation import BeamformingSimulator


class MainController:
    def __init__(self, app):
        self.app = app
        self.main_window = QtWidgets.QMainWindow()

        self.logging = LoggingManager()  # Singleton instance
        self.logging.log("Controller Initializing...")

        self.view = Ui_MainWindow()
        self.initialize_view()
        self.initialize_arrays_info()
        
        self.logging.log("Controller Initialized Successfully.")

    def initialize_view(self):
        self.view.setupUi(self.main_window)
        self.view.scenarios_button.clicked.connect(self.toggle_scenario)
        self.current_scenario = None

        self.view.elements_number_SpinBox.editingFinished.connect(self.update_current_elements_number)

        self.view.elements_spacing_slider.valueChanged.connect(self.update_elements_spacing)
        
        self.view.array_curve_slider.valueChanged.connect(self.update_elements_curvature)
        
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

        self.logging.log_action(f"User switched scenario to: {self.current_scenario}")

        scenario = scenario_settings[self.current_scenario]

        self.view.operating_frequency_spinbox.setValue(scenario['frequency'])
        self.view.operating_frequency_range_combobox.setCurrentIndex(scenario['frequency_bandwidth_index'])
        self.update_operating_frequency()

        self.view.elements_spacing_slider.setValue(scenario['elements_spacing'])
        self.update_elements_spacing()

        self.view.array_curve_slider.setValue(scenario['curvature'])
        self.update_elements_curvature()

        self.view.elements_number_SpinBox.setValue(scenario['num_elements'])
        self.update_current_elements_number()

        self.view.scenarios_button.setText(f"{self.current_scenario}")
        self.view.updateVisualization()
        self.update_and_refresh_arrays_info()

    def initialize_arrays_info(self):
        self.configurations = []
        try:
            spacing, num_elements, curvature = self.view.visualization_widget.get_array_configuration(1)
        except Exception as e:
            self.logging.log_warning(f"Could not get initial array config, using defaults. Error: {e}")
            spacing, num_elements, curvature = (self.view.current_elements_spacing * 10, self.view.current_elements_number, self.view.current_array_curvature_angle)

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
        if x_coords:
            x_min, x_max = min(x_coords), max(x_coords)
            y_min, y_max = min(y_coords), max(y_coords)
            x_padding = spacing * 0.5 if spacing > 0 else 1
            y_range = y_max - y_min
            y_padding = y_range * 0.5 if y_range > 0 else 1
            self.view.arrayShapeItem.setXRange(x_min - x_padding, x_max + x_padding, padding=0)
            self.view.arrayShapeItem.setYRange(y_min - y_padding, y_max + y_padding, padding=0)

    def update_and_refresh_arrays_info(self):
        self.configurations.clear()
        # Only Array 1 is currently active in the simplified logic, but iterating for safety
        for i in range(1, self.view.current_arrays_number + 1):
            try:
                spacing, num_elements, curvature = self.view.visualization_widget.get_array_configuration(i)
                self.configurations.append({'num_elements': num_elements, 'spacing': spacing, 'curvature': curvature})
            except IndexError:
                # self.logging.log_warning(f"Skipping config for inactive array {i}")
                pass
        
        self.array_visualize(self.view.current_elements_number, self.view.elements_spacing_slider.value(), self.view.current_array_curvature_angle)
        self.apply_configurations_to_visualization()

    def apply_configurations_to_visualization(self):
        self.model.arrays_configurations = self.configurations
        self.model.operating_frequency = self.view.current_operating_frequency
        self.model.steering_angle = self.view.current_steering_angle

        try:
            x, y, intensity = self.model.simulate_multiple_arrays((-10, 10), (0, 10))

            angles = np.linspace(-90, 90, 500)
            array_factor = self.model.calculate_array_factor(angles)

            self.view.intensityImageItem.clear()
            self.view.beamProfileLine.clear()
            self.view.intensityImageItem.setImage(intensity.T)
            self.view.intensityImageItem.setLevels([np.min(intensity), np.max(intensity)])
            self.view.beamProfileLine.setData(angles, array_factor)
        except Exception as e:
            self.logging.log_error(f"Simulation Update Failed: {e}", exc_info=True)

    def update_current_elements_number(self):
        self.view.current_elements_number = self.view.elements_number_SpinBox.value()
        self.logging.log_action(f"Elements Number updated to: {self.view.current_elements_number}")
        self.view.updateVisualization()
        self.update_and_refresh_arrays_info()
        self.view.arrays_parameters_indicator.setText(f"{self.view.current_elements_number} Elements")

    def update_elements_spacing(self):
        if self.view.current_operating_frequency > 0:
            self.view.current_elements_spacing = (self.view.elements_spacing_slider.value() / 100) * self.model.wavelength
        else:
            self.view.current_elements_spacing = 0
            
        # Log this frequently? Maybe debug
        self.logging.log_debug(f"Spacing updated. Slider: {self.view.elements_spacing_slider.value()}")
        
        self.view.updateVisualization()
        self.update_and_refresh_arrays_info()
        self.view.arrays_parameters_indicator.setText(f"{self.view.elements_spacing_slider.value()}% Wavelength")

    def update_elements_curvature(self):
        self.view.current_array_curvature_angle = self.view.array_curve_slider.value()
        self.logging.log_debug(f"Curvature updated to: {self.view.current_array_curvature_angle}")
        self.view.updateVisualization()
        self.update_and_refresh_arrays_info()
        self.view.arrays_parameters_indicator.setText(f"{self.view.current_array_curvature_angle} Degree")

    def update_steering_angle(self):
        self.view.current_steering_angle = self.view.steering_angle_slider.value()
        self.logging.log_debug(f"Steering angle updated to: {self.view.current_steering_angle}")
        self.model.update_steering_angle(self.view.current_steering_angle)
        self.apply_configurations_to_visualization()
        self.view.sidebar_parameter_indicator.setText(f"{self.view.current_steering_angle} Degree")

    def update_operating_frequency(self):
        index = self.view.operating_frequency_range_combobox.currentIndex()
        if index < 0: index = 0
        range_val = 10 ** (3 * (index + 1))
        self.view.current_operating_frequency = self.view.operating_frequency_spinbox.value() * range_val
        
        self.logging.log_action(f"Operating Frequency updated to: {self.view.current_operating_frequency:.2e} Hz")
        
        self.model.update_operating_frequency(self.view.current_operating_frequency)
        self.apply_configurations_to_visualization()
        self.view.sidebar_parameter_indicator.setText(self.view.format_frequency(self.view.current_operating_frequency))

    def update_spacing_frequency(self):
        self.update_operating_frequency()
        self.update_elements_spacing()

    def clean_project(self):
        project_root = os.getcwd()
        self.logging.log("Starting project cleanup...")

        # 1. Remove .idea, __pycache__, .DS_Store
        for root, dirs, files in os.walk(project_root):
             if "__pycache__" in dirs:
                 shutil.rmtree(os.path.join(root, "__pycache__"))
             
             if ".DS_Store" in files:
                 os.remove(os.path.join(root, ".DS_Store"))

        idea_path = os.path.join(project_root, ".idea")
        if os.path.exists(idea_path):
             shutil.rmtree(idea_path)

        # 2. Generate .gitignore
        gitignore_path = os.path.join(project_root, ".gitignore")
        gitignore_content = ".idea/\n__pycache__/\n*.pyc\n*.DS_Store\n.venv/\n.env\nlogging/\n" # Added logging/ to ignore logs
        with open(gitignore_path, "w") as f:
            f.write(gitignore_content)
        
        self.logging.log("Project cleanup complete and .gitignore generated.")

    def close_application(self):
        self.clean_project()
        self.logging.log(f"Application Closed normally.")
        self.main_window.close()

    def run(self):
        self.logging.log("Main Window Showing FullScreen")
        self.main_window.showFullScreen()
        return self.app.exec_()
