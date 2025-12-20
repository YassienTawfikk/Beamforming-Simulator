from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import pyqtgraph as pg
from app.ui.array_visualization_widget import ArrayVisualizationWidget


class Ui_MainWindow(object):
    def __init__(self, current_selected_ALL_array=True, current_arrays_number=1, current_array_curvature_angle=0,
                 current_elements_number=2, current_elements_spacing=0.05, current_steering_angle=0,
                 current_operating_frequency=100e3):
        self.visualization_widget = ArrayVisualizationWidget()

        self.BUTTON_STYLESHEET = """
        QPushButton {
            color: #E0E0E0;
            background-color: rgba(255, 255, 255, 0.05);
            border: 1px solid #546E7A;
            border-radius: 6px;
            font-size: 14px;
            padding: 5px;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 0.1);
            border-color: #81D4FA;
        }
        QPushButton:pressed {
            background-color: rgba(255, 255, 255, 0.15);
        }
        """

        self.QUIT_BUTTON_STYLESHEETSHEET = """
        QPushButton {
            color: rgb(8, 51, 143);
            background-color: rgba(255, 255, 255, 0);
            border: 3px solid rgb(8, 51, 143)
        }
        QPushButton:hover {
            border-color: rgb(253, 94, 80);
            color: rgb(253, 94, 80);
        }
        """
        self.SCENARIOS_BUTTON_STYLESHEETSHEET = """
        QPushButton {
            color: #42A5F5;
            background-color: transparent;
            border: 2px solid #42A5F5;
            border-radius: 6px;
            font-weight: bold;
        }
        QPushButton:hover {
            background-color: #42A5F5;
            color: white;
        }
        """
        self.SLIDER_STYLESHEET = """
        QSlider::groove:horizontal {
            border: 1px solid #37474F;
            height: 6px;
            background: #263238;
            margin: 2px 0;
            border-radius: 3px;
        }
        QSlider::handle:horizontal {
            background: #29B6F6;
            border: 1px solid #29B6F6;
            width: 18px;
            height: 18px;
            margin: -7px 0;
            border-radius: 9px;
        }
        QSlider::handle:horizontal:hover {
            background: #4FC3F7;
        }
        QSlider::sub-page:horizontal {
            background: #0288D1;
            border-radius: 3px;
        }
        """
        self.SPINBOX_STYLESHEET = """
        QSpinBox {
            background-color: #263238;
            color: #ECEFF1;
            border: 1px solid #546E7A;
            border-radius: 4px;
            padding: 6px;
            font-size: 14px;
        }
        QSpinBox:hover {
            border: 1px solid #81D4FA;
        }
        QSpinBox::up-button {
            subcontrol-origin: border;
            subcontrol-position: top right;
            width: 20px;
            border-left: 1px solid #546E7A;
            background: #37474F;
            border-top-right-radius: 4px;
        }
        QSpinBox::down-button {
            subcontrol-origin: border;
            subcontrol-position: bottom right;
            width: 20px;
            border-left: 1px solid #546E7A;
            background: #37474F;
            border-bottom-right-radius: 4px;
        }
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {
            background: #455A64;
        }
        QSpinBox::up-arrow {
            width: 10px;
            height: 10px;
            image: url("./static/Up_Arrow.png");
            border: none;
        }
        QSpinBox::down-arrow {
            width: 10px;
            height: 10px;
            image: url("./static/Down_Arrow.png");
            border: none;
        }
        """
        self.COMBOBOX_STYLESHEET = """
        QComboBox {
            background-color: #263238;
            color: #ECEFF1;
            border: 1px solid #546E7A;
            border-radius: 4px;
            padding: 6px;
            padding-left: 10px;
            font-size: 14px;
            min-width: 300px;
        }
        QComboBox:hover {
            border: 1px solid #81D4FA;
        }
        QComboBox::drop-down {
            subcontrol-origin: padding;
            subcontrol-position: top right;
            width: 25px;
            border-left-width: 1px;
            border-left-color: #546E7A;
            border-left-style: solid;
            border-top-right-radius: 4px;
            border-bottom-right-radius: 4px;
            background: #37474F;
        }
        QComboBox::down-arrow {
            image: url("./static/Down_Arrow.png");
            width: 10px;
            height: 10px;
        }
        QComboBox QAbstractItemView {
            background-color: #37474F;
            color: #ECEFF1;
            selection-background-color: #0288D1;
            border: 1px solid #546E7A;
        }
        """

        self.sidebar_open = False
        self.current_selected_ALL_array = current_selected_ALL_array
        self.current_arrays_number = current_arrays_number
        self.current_selected_array = 1
        self.current_array_curvature_angle = current_array_curvature_angle
        self.current_elements_number = current_elements_number
        self.current_elements_spacing = current_elements_spacing
        self.current_steering_angle = current_steering_angle
        self.current_operating_frequency = current_operating_frequency

        self.operating_frequency_ranges = ['Kilo', 'Mega', 'Giga', 'Tera', 'Peta']

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 800)
        MainWindow.setFont(QtGui.QFont("Noto Serif Balinese"))
        MainWindow.setStyleSheet("background-color:#1A1A40")

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        MainWindow.setCentralWidget(self.centralwidget)

        # Main Vertical Layout
        self.main_layout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        # 1. Title/Header Bar
        self.setupTitleBar()
        self.main_layout.addLayout(self.title_layout)

        # 2. Main Inputs Bar (Arrays, Elements, etc.) - Placed at Top (Row 2 equivalent)
        self.setupInputsBar()
        self.main_layout.addLayout(self.inputs_layout)

        # 3. Visualization Area (Graphs + Sidebar Controls)
        self.setupVisualizationArea()
        self.main_layout.addWidget(self.graphsContainer)

        self.setupMainButtons()
        self.setupMenuBar(MainWindow)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setupTitleBar(self):
        self.title_layout = QtWidgets.QHBoxLayout()
        self.title_icon = self.createLabel(self.title_layout, "./static/Sensor.png", 50)
        self.title_label = self.createLabel(self.title_layout, text_font=("PT Sans", 20), max_size=(370, 50))
        
        self.title_layout.addStretch()
        
        self.scenarios_button = QtWidgets.QPushButton()
        self.scenarios_button.setMinimumSize(110, 40)
        self.scenarios_button.setFont(QtGui.QFont("Hiragino Sans GB", 13, True))
        self.scenarios_button.setStyleSheet(self.SCENARIOS_BUTTON_STYLESHEETSHEET)
        self.scenarios_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.scenarios_button.setText("Scenarios")
        self.title_layout.addWidget(self.scenarios_button)

        self.quit_app_button = QtWidgets.QPushButton()
        self.quit_app_button.setFixedSize(40, 40)
        self.quit_app_button.setFont(QtGui.QFont("Hiragino Sans GB", 20, True))
        self.quit_app_button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.quit_app_button.setStyleSheet(self.QUIT_BUTTON_STYLESHEETSHEET)
        self.quit_app_button.setText("X")
        self.title_layout.addWidget(self.quit_app_button)

    def setupInputsBar(self):
        self.inputs_layout = QtWidgets.QHBoxLayout()
        self.inputs_layout.setContentsMargins(0, 0, 0, 0)
        # Buttons will be added here by setupMainButtons

    def setupVisualizationArea(self):
        # Container Widget for Graphs
        self.graphsContainer = QtWidgets.QWidget()
        self.graphsContainer.setStyleSheet("""
            QWidget {
                background-color: rgba(34, 34, 68, 255);
                color: #E0E0E0;
                border: 1px solid #B0BEC5;
            }
        """)
        
        # Vertical layout inside visual area: Graphs Top, Sidebar Controls Bottom
        area_layout = QtWidgets.QVBoxLayout(self.graphsContainer)
        
        # Grid for Plots
        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setStyleSheet("border: none;")
        self.plots_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        area_layout.addWidget(self.gridLayoutWidget, stretch=1)

        self.setupPlotHolders()

        # Sidebar Controls (Frequency, Steering) - Originally at bottom of visual area
        self.controls_widget = QtWidgets.QWidget()
        self.controls_widget.setMaximumHeight(80)
        self.controls_widget.setStyleSheet("border: none;")
        self.controls_layout = QtWidgets.QHBoxLayout(self.controls_widget)
        
        # Center the controls
        self.controls_layout.addStretch()
        
        # Add buttons/sliders to controls layout
        self.return_sidebar_buttons = self.createButton(self.controls_layout, "Back", isVisible=False,
                                                        method=self.return_sidebar_initial_button)
        self.steering_angle_button = self.createButton(self.controls_layout, "Steering Angle", method=self.show_steering_angle_slider)
        self.steering_angle_slider = self.createSlider(self.controls_layout, min_value=-70, max_value=70,
                                                       initial_value=self.current_steering_angle, isVisible=False)
        self.operating_frequency_button = self.createButton(self.controls_layout, "Operating Frequency", method=self.show_frequency_combobox)
        self.operating_frequency_spinbox = self.createSpinBox(self.controls_layout, min_value=1, max_value=999, initial_value=100,
                                                              isVisible=False)
        self.operating_frequency_range_combobox = self.createComboBox(self.controls_layout, options=self.operating_frequency_ranges,
                                                                      isVisible=False)
        self.sidebar_parameter_indicator = self.createLabel(self.controls_layout, max_size=150, isVisible=False)

        self.SIDEBAR_CONTROLLER_BUTTONS = [
            self.return_sidebar_buttons, self.steering_angle_button, self.steering_angle_slider,
            self.operating_frequency_button, self.operating_frequency_range_combobox,
            self.operating_frequency_spinbox, self.sidebar_parameter_indicator
        ]
        
        # Center the controls
        self.controls_layout.addStretch()
        
        area_layout.addWidget(self.controls_widget)

        # Init Visualization
        spacing_factor = 10
        self.visualization_widget.addArray(
            spacing=self.current_elements_spacing * spacing_factor,
            num_elements=self.current_elements_number,
            curvature_angle=self.current_array_curvature_angle,
        )

    def setupPlotHolders(self):
        # We can implement this simply by adding pg widgets to the grid
        # Left: Intensity Map
        self.graphWidget1 = pg.GraphicsLayoutWidget()
        self.graphWidget1.setBackground('#1A1A40')
        self.plots_layout.addWidget(self.graphWidget1, 0, 0)

        # Right: Beam Profile & Array Shape
        self.graphWidget2 = pg.GraphicsLayoutWidget()
        self.graphWidget2.setBackground('#1A1A40')
        self.plots_layout.addWidget(self.graphWidget2, 0, 1)

        # Setup Intensity Map
        self.intensityMapItem = self.graphWidget1.addPlot(title="Intensity Map")
        self.intensityMapItem.setLabel('left', 'Frequency', color='w')
        self.intensityMapItem.setLabel('bottom', 'Time', color='w')
        self.intensityImageItem = pg.ImageItem()
        self.intensityMapItem.addItem(self.intensityImageItem)
        
        colormap = pg.colormap.get('seismic', source='matplotlib')
        self.intensityImageItem.setLookupTable(colormap.getLookupTable())
        
        colorBar = pg.ColorBarItem(interactive=False, colorMap=colormap)
        colorBar.setImageItem(self.intensityImageItem)
        self.graphWidget1.addItem(colorBar)

        # Setup Beam Profile (Right, Top)
        self.beamProfileItem = self.graphWidget2.addPlot(row=0, col=0, title="Beam Profile")
        self.beamProfileItem.setLabel('left', 'Array Factor')
        self.beamProfileItem.setLabel('bottom', 'Angle')
        self.beamProfileItem.showGrid(x=True, y=True, alpha=0.2)
        self.beamProfileLine = self.beamProfileItem.plot(pen=pg.mkPen(color='w', width=2))

        # Setup Array Shape (Right, Bottom)
        self.arrayShapeItem = self.graphWidget2.addPlot(row=1, col=0, title="Array Shape")
        self.arrayShapeItem.showGrid(x=True, y=True, alpha=0.3)

    def setupMainButtons(self):
        # Center the buttons
        self.inputs_layout.addStretch()
        
        self.return_main_buttons = self.createButton(self.inputs_layout, "Back", self.return_main_initial_button, isVisible=False)
        self.current_selected_array_button = self.createButton(self.inputs_layout, "Array 1", self.toggle_current_selected_array,
                                                               isVisible=False)

        # REMOVED: Adjust Array Number Button and SpinBox
        # self.adjust_array_number = self.createButton(self.inputs_layout, "Arrays Number", self.show_arrays_number_SpinBox)
        # self.arrays_number_SpinBox = self.createSpinBox(self.inputs_layout, min_value=1, max_value=8, initial_value=self.current_arrays_number,
        #                                                 isVisible=False)

        self.elements_number_button = self.createButton(self.inputs_layout, "Elements Number", self.show_elements_number_SpinBox)
        self.elements_number_SpinBox = self.createSpinBox(self.inputs_layout, min_value=2, max_value=128,
                                                          initial_value=self.current_elements_number, isVisible=False)

        self.elements_spacing_button = self.createButton(self.inputs_layout, "Elements Spacing", self.show_spacing_input)
        self.elements_spacing_slider = self.createSlider(layout=self.inputs_layout, min_value=1, max_value=50,
                                                         initial_value=int(self.current_elements_spacing * 100), isVisible=False)

        self.add_curve_button = self.createButton(self.inputs_layout, "Array Curve", self.show_curve_input)
        self.array_curve_slider = self.createSlider(layout=self.inputs_layout, min_value=0, max_value=180, initial_value=0, isVisible=False)

        self.arrays_parameters_indicator = self.createLabel(self.inputs_layout, max_size=110, isVisible=False)

        self.ARRAYS_CONTROLLER_BUTTONS = [self.return_main_buttons, self.array_curve_slider, 
                                          self.elements_number_button,
                                          self.elements_spacing_button, self.add_curve_button, self.elements_spacing_slider,
                                          self.elements_number_SpinBox, self.current_selected_array_button,
                                          self.arrays_parameters_indicator]
                                          
        # Center the buttons
        self.inputs_layout.addStretch()

    def setupMenuBar(self, MainWindow):
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        MainWindow.setMenuBar(self.menubar)

    # --- Helper Methods ---
    def createLabel(self, layout, pixmap=None, max_size=50, text_font=None, isVisible=True):
        label = QtWidgets.QLabel()
        if pixmap and isinstance(pixmap, str):
            label.setPixmap(QtGui.QPixmap(pixmap))
        if text_font:
            font = QtGui.QFont()
            font.setFamily(text_font[0])
            font.setPointSize(text_font[1])
            label.setFont(font)
        label.setStyleSheet("color:white")
        label.setMaximumSize(QtCore.QSize(*([max_size] * 2 if isinstance(max_size, int) else max_size)))
        label.setScaledContents(True)
        if hasattr(layout, 'addWidget'):
            layout.addWidget(label)
        elif hasattr(layout, 'addLayout'): 
             layout.addWidget(label)
             
        if not isVisible:
            label.hide()
        return label

    def createButton(self, layout, text, method=None, isVisible=True):
        button = QtWidgets.QPushButton()
        button.setMinimumSize(QtCore.QSize(150, 40))
        button.setMaximumSize(QtCore.QSize(150, 40))
        button.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        button.setStyleSheet(self.BUTTON_STYLESHEET)
        button.setText(text)
        layout.addWidget(button)
        
        if method:
            button.clicked.connect(method)
            
        if not isVisible:
            button.hide()
        return button

    def createSlider(self, layout, min_value=0, max_value=100, initial_value=50, orientation=QtCore.Qt.Horizontal, isVisible=True):
        slider = QtWidgets.QSlider(orientation)
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(initial_value)
        slider.setMaximumWidth(200)
        slider.setStyleSheet(self.SLIDER_STYLESHEET)
        layout.addWidget(slider)

        if not isVisible:
            slider.hide()
        return slider

    def createSpinBox(self, layout, min_value=0, max_value=100, initial_value=50, isVisible=True):
        spin_box = QtWidgets.QSpinBox()
        spin_box.setMinimum(min_value)
        spin_box.setMaximum(max_value)
        spin_box.setValue(initial_value)
        spin_box.setMaximumSize(260, 40)
        spin_box.setStyleSheet(self.SPINBOX_STYLESHEET)
        layout.addWidget(spin_box)

        if not isVisible:
            spin_box.hide()
        return spin_box

    def createComboBox(self, layout, options, default_value=None, isEditable=False, isVisible=True):
        combo_box = QtWidgets.QComboBox()
        combo_box.addItems(options)
        combo_box.setEditable(isEditable)
        combo_box.setMaximumSize(300, 40)
        combo_box.setStyleSheet(self.COMBOBOX_STYLESHEET)
        layout.addWidget(combo_box)

        if not isVisible:
            combo_box.hide()
        return combo_box
        
    def format_frequency(self, freq):
        if freq is None: return "Frequency not set"
        def format_value(value, unit):
             if int(value) == value: return f"{int(value)} {unit}"
             return f"{value:.2f} {unit}"
        if freq < 0: return "Invalid"
        if freq >= 1e15: return format_value(freq / 1e15, "PHz")
        elif freq >= 1e12: return format_value(freq / 1e12, "THz")
        elif freq >= 1e9: return format_value(freq / 1e9, "GHz")
        elif freq >= 1e6: return format_value(freq / 1e6, "MHz")
        elif freq >= 1e3: return format_value(freq / 1e3, "KHz")
        elif freq > 0: return format_value(freq, "Hz")
        return "0 Hz"

    # --- Menu Logic (Restored) ---
    def return_main_initial_button(self):
        if self.return_main_buttons.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            self.show_button([self.elements_number_button, self.elements_spacing_button,
                              self.add_curve_button])

    def return_sidebar_initial_button(self):
        if self.return_sidebar_buttons.isVisible():
            self.hide_button(self.SIDEBAR_CONTROLLER_BUTTONS)
            self.show_button([self.operating_frequency_button, self.steering_angle_button])

    def toggle_current_selected_array(self):
        if self.current_selected_ALL_array:
            self.current_selected_ALL_array = not self.current_selected_ALL_array
        next_selected_array = self.current_selected_array
        if next_selected_array <= self.current_arrays_number:
            self.current_selected_array_button.setText(f"Array {next_selected_array}")
        else:
            self.current_selected_ALL_array = True
            self.current_selected_array_button.setText("All Arrays")

    def show_curve_input(self):
        if not self.array_curve_slider.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            self.arrays_parameters_indicator.setText(f"{self.current_array_curvature_angle} Degree")
            controller_buttons = [self.return_main_buttons, self.array_curve_slider, self.arrays_parameters_indicator]
            self.show_button(controller_buttons)

    def show_spacing_input(self):
        if not self.elements_spacing_slider.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            controller_buttons = [self.return_main_buttons, self.elements_spacing_slider, self.arrays_parameters_indicator]
            self.show_button(controller_buttons)
            self.arrays_parameters_indicator.setText(f"{self.elements_spacing_slider.value()} % wavelength")

    # Removed: show_arrays_number_SpinBox

    def show_elements_number_SpinBox(self):
        if not self.elements_number_SpinBox.isVisible():
            self.hide_button(self.ARRAYS_CONTROLLER_BUTTONS)
            self.arrays_parameters_indicator.setText(f"{self.current_elements_number} Elements")
            controller_buttons = [self.return_main_buttons, self.elements_number_SpinBox, self.arrays_parameters_indicator]
            self.show_button(controller_buttons)

    def show_frequency_combobox(self):
        if not self.operating_frequency_range_combobox.isVisible():
            self.hide_button(self.SIDEBAR_CONTROLLER_BUTTONS)
            controller_buttons = [self.return_sidebar_buttons, self.operating_frequency_spinbox, self.operating_frequency_range_combobox,
                                  self.sidebar_parameter_indicator]
            self.show_button(controller_buttons)
            formatted_frequency = self.format_frequency(self.current_operating_frequency)
            self.sidebar_parameter_indicator.setText(formatted_frequency)

    def show_steering_angle_slider(self):
        if not self.steering_angle_slider.isVisible():
            self.hide_button(self.SIDEBAR_CONTROLLER_BUTTONS)
            controller_buttons = [self.return_sidebar_buttons, self.steering_angle_slider, self.sidebar_parameter_indicator]
            self.show_button(controller_buttons)
            self.sidebar_parameter_indicator.setText(f"{self.current_steering_angle} Degree")

    def hide_button(self, buttons):
        for button in buttons:
            if button.isVisible():
                button.hide()

    def show_button(self, buttons):
        for button in buttons:
            if not button.isVisible():
                button.show()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Transmitter Beamforming Simulator"))
        self.title_label.setText(_translate("MainWindow", "Transmitter Beamforming Simulator"))

    def updateVisualization(self):
        spacing_factor = 5
        self.visualization_widget.editArray(
             index=1,
             spacing=self.current_elements_spacing * spacing_factor,
             num_elements=self.current_elements_number,
             curvature_angle=self.current_array_curvature_angle
        )
