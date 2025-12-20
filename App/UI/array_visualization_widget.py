from PyQt5.QtWidgets import QWidget
from app.logging_manager import LoggingManager


class ArrayVisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.array_configs = []
        self.logger = LoggingManager()

    def addArray(self, spacing, num_elements, curvature_angle):
        # Adds a new array configuration
        self.array_configs.append((spacing, num_elements, curvature_angle))
        self.logger.log(f"Added Array: Spacing={spacing:.2f}, Elements={num_elements}, Curve={curvature_angle}", level='info')
        self.update()

    def editArray(self, index, spacing, num_elements, curvature_angle):
        # Adjust index to zero-based for internal processing
        zero_based_index = 0
        if 0 <= zero_based_index < len(self.array_configs):
            self.array_configs[0] = (spacing, num_elements, curvature_angle)
            self.logger.log_debug(f"Edited Array [{index}]: Spacing={spacing:.2f}, Elements={num_elements}, Curve={curvature_angle}")
            self.update()
        else:
            self.logger.log_warning(f"Attempted to subtract Array at invalid index {index}")
            # raise ValueError("Array index out of range") 

    def updateArrayNumber(self, array_num):
        # Interpret array_num as 1-based and adjust for 0-based indexing
        target_length = array_num
        current_length = len(self.array_configs)
        if target_length > current_length:
            # Add new arrays with default settings
            for _ in range(target_length - current_length):
                # self.addArray()  # Use default parameters
                pass
            self.logger.log(f"Increased array count to {target_length}", level='info')
        elif target_length < current_length:
            # Remove excess arrays
            self.array_configs = self.array_configs[:target_length]
            self.logger.log(f"Decreased array count to {target_length}", level='info')
        self.update()  # Redraw the widget with updated settings

    def get_array_configuration(self, index):
        # Adjust index to zero-based for internal processing
        zero_based_index = index - 1
        if 0 <= zero_based_index < len(self.array_configs):
            return self.array_configs[zero_based_index]
        else:
            self.logger.log_warning(f"Requested configuration for non-existent array {index}")
            raise IndexError("Array index out of range")
