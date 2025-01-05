from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import QPoint
from math import cos, radians, sin


class ArrayVisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.array_configs = []

    def addArray(self, spacing, num_elements, curvature_angle):
        # Adds a new array configuration
        self.array_configs.append((spacing, num_elements, curvature_angle))
        self.update()

    def editArray(self, index, spacing, num_elements, curvature_angle):
        # Adjust index to zero-based for internal processing
        zero_based_index = 0
        if 0 <= zero_based_index < len(self.array_configs):
            self.array_configs[0] = (spacing, num_elements, curvature_angle)
            self.update()
        else:
            raise ValueError("Array index out of range")  # Provide feedback for invalid index

    def updateArrayNumber(self, array_num):
        # Interpret array_num as 1-based and adjust for 0-based indexing
        target_length = array_num
        current_length = len(self.array_configs)
        if target_length > current_length:
            # Add new arrays with default settings
            for _ in range(target_length - current_length):
                # self.addArray()  # Use default parameters
                pass
        elif target_length < current_length:
            # Remove excess arrays
            self.array_configs = self.array_configs[:target_length]
        self.update()  # Redraw the widget with updated settings

    def get_array_configuration(self, index):
        # Adjust index to zero-based for internal processing
        zero_based_index = index - 1
        if 0 <= zero_based_index < len(self.array_configs):
            return self.array_configs[zero_based_index]
        else:
            raise IndexError("Array index out of range")
