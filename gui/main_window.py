from PyQt5.QtWidgets import (QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, 
                             QWidget, QLineEdit, QLabel, QFileDialog, QStatusBar, 
                             QGroupBox, QGridLayout, QSlider, QDoubleSpinBox, QCheckBox)
from PyQt5.QtCore import Qt
from gui.opengl_widget import GLWidget

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quaternion Visualizer")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready - Load a .obj file to get started")

        # Create main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)
        
        # Create OpenGL widget (main view)
        self.opengl_widget = GLWidget()
        self.opengl_widget.setMinimumSize(600, 400)
        
        # Create control panel
        control_panel = self.create_control_panel()
        
        # Add to main layout
        main_layout.addWidget(self.opengl_widget, 2)  # Give more space to 3D view
        main_layout.addWidget(control_panel, 1)
        
        # Initialize visualization settings
        self.update_visualizations()

    def create_control_panel(self):
        panel = QWidget()
        panel.setMaximumWidth(300)
        layout = QVBoxLayout(panel)
        
        # File operations group
        file_group = QGroupBox("File Operations")
        file_layout = QVBoxLayout(file_group)
        
        self.load_button = QPushButton("Load 3D Object (.obj)")
        self.load_button.clicked.connect(self.load_obj)
        file_layout.addWidget(self.load_button)
        
        # Add demo button
        self.demo_button = QPushButton("Load Demo Car")
        self.demo_button.clicked.connect(self.load_demo_car)
        file_layout.addWidget(self.demo_button)
        
        # Object info label
        self.object_info_label = QLabel("No object loaded")
        self.object_info_label.setWordWrap(True)
        file_layout.addWidget(self.object_info_label)
        
        layout.addWidget(file_group)
        
        # Rotation controls group
        rotation_group = QGroupBox("Quaternion Rotation")
        rotation_layout = QGridLayout(rotation_group)
        
        # Axis inputs
        rotation_layout.addWidget(QLabel("Rotation Axis:"), 0, 0, 1, 2)
        
        rotation_layout.addWidget(QLabel("X:"), 1, 0)
        self.axis_x_input = QDoubleSpinBox()
        self.axis_x_input.setRange(-1000.0, 1000.0)  # Much larger range
        self.axis_x_input.setValue(1.0)
        self.axis_x_input.setDecimals(3)
        self.axis_x_input.setSingleStep(0.1)
        self.axis_x_input.setKeyboardTracking(True)  # Enable immediate keyboard input
        rotation_layout.addWidget(self.axis_x_input, 1, 1)
        
        rotation_layout.addWidget(QLabel("Y:"), 2, 0)
        self.axis_y_input = QDoubleSpinBox()
        self.axis_y_input.setRange(-1000.0, 1000.0)  # Much larger range
        self.axis_y_input.setValue(0.0)
        self.axis_y_input.setDecimals(3)
        self.axis_y_input.setSingleStep(0.1)
        self.axis_y_input.setKeyboardTracking(True)  # Enable immediate keyboard input
        rotation_layout.addWidget(self.axis_y_input, 2, 1)
        
        rotation_layout.addWidget(QLabel("Z:"), 3, 0)
        self.axis_z_input = QDoubleSpinBox()
        self.axis_z_input.setRange(-1000.0, 1000.0)  # Much larger range
        self.axis_z_input.setValue(0.0)
        self.axis_z_input.setDecimals(3)
        self.axis_z_input.setSingleStep(0.1)
        self.axis_z_input.setKeyboardTracking(True)  # Enable immediate keyboard input
        rotation_layout.addWidget(self.axis_z_input, 3, 1)
        
        # Angle input
        rotation_layout.addWidget(QLabel("Angle (degrees):"), 4, 0)
        self.angle_input = QDoubleSpinBox()
        self.angle_input.setRange(-360.0, 360.0)
        self.angle_input.setValue(45.0)
        self.angle_input.setDecimals(1)
        self.angle_input.setSingleStep(5.0)
        rotation_layout.addWidget(self.angle_input, 4, 1)
        
        # Rotation buttons
        self.rotate_button = QPushButton("Apply Rotation")
        self.rotate_button.clicked.connect(self.apply_rotation)
        rotation_layout.addWidget(self.rotate_button, 5, 0, 1, 2)
        
        layout.addWidget(rotation_group)
        
        # Visualization controls group
        viz_group = QGroupBox("Visualization Options")
        viz_layout = QVBoxLayout(viz_group)
        
        # Object visibility controls
        self.show_original_checkbox = QCheckBox("Show Original Object")
        self.show_original_checkbox.setChecked(True)
        self.show_original_checkbox.stateChanged.connect(self.update_visualizations)
        viz_layout.addWidget(self.show_original_checkbox)
        
        self.show_rotated_checkbox = QCheckBox("Show Rotated Object")
        self.show_rotated_checkbox.setChecked(True)
        self.show_rotated_checkbox.stateChanged.connect(self.update_visualizations)
        viz_layout.addWidget(self.show_rotated_checkbox)
        
        # Separator
        separator = QLabel("─" * 25)
        separator.setStyleSheet("color: gray;")
        viz_layout.addWidget(separator)
        
        self.show_axes_checkbox = QCheckBox("Show Coordinate Axes (XYZ)")
        self.show_axes_checkbox.setChecked(True)
        self.show_axes_checkbox.stateChanged.connect(self.update_visualizations)
        viz_layout.addWidget(self.show_axes_checkbox)
        
        self.show_rotation_axis_checkbox = QCheckBox("Show Rotation Axis")
        self.show_rotation_axis_checkbox.setChecked(True)
        self.show_rotation_axis_checkbox.stateChanged.connect(self.update_visualizations)
        viz_layout.addWidget(self.show_rotation_axis_checkbox)
        
        self.show_angle_label_checkbox = QCheckBox("Show Rotation Angle")
        self.show_angle_label_checkbox.setChecked(True)
        self.show_angle_label_checkbox.stateChanged.connect(self.update_visualizations)
        viz_layout.addWidget(self.show_angle_label_checkbox)
        
        layout.addWidget(viz_group)
        
        # View controls group
        view_group = QGroupBox("View Controls")
        view_layout = QVBoxLayout(view_group)
        
        self.reset_button = QPushButton("Reset View")
        self.reset_button.clicked.connect(self.opengl_widget.reset_view)
        view_layout.addWidget(self.reset_button)
        
        help_label = QLabel("Mouse Controls:\n• Left drag: Rotate view\n• Wheel: Zoom in/out")
        help_label.setStyleSheet("color: gray; font-size: 10px;")
        view_layout.addWidget(help_label)
        
        layout.addWidget(view_group)
        
        # Add stretch to push everything to top
        layout.addStretch()
        
        return panel

    def load_obj(self):
        """Load a 3D object file"""
        filename, _ = QFileDialog.getOpenFileName(
            self, 
            "Open 3D Object", 
            "obj/",  # Start in obj directory
            "OBJ Files (*.obj);;All Files (*)"
        )
        if filename:
            self.status_bar.showMessage("Loading object...")
            success = self.opengl_widget.load_mesh(filename)
            
            if success:
                # Update object info
                import os
                obj_name = os.path.basename(filename)
                if self.opengl_widget.mesh:
                    vertex_count = len(self.opengl_widget.mesh.vertices)
                    face_count = len(self.opengl_widget.mesh.faces)
                    self.object_info_label.setText(
                        f"Loaded: {obj_name}\n"
                        f"Vertices: {vertex_count:,}\n"
                        f"Faces: {face_count:,}"
                    )
                    self.status_bar.showMessage(f"Successfully loaded {obj_name}")
                else:
                    self.object_info_label.setText("Failed to load object")
                    self.status_bar.showMessage("Failed to load object")
            else:
                self.object_info_label.setText("Failed to load object")
                self.status_bar.showMessage("Failed to load object")

    def apply_rotation(self):
        """Apply quaternion rotation to the loaded object"""
        if self.opengl_widget.mesh is None:
            self.status_bar.showMessage("Please load an object first")
            return
            
        try:
            axis = [
                self.axis_x_input.value(),
                self.axis_y_input.value(), 
                self.axis_z_input.value()
            ]
            angle = self.angle_input.value()
            
            # Check if axis is valid (not zero vector)
            axis_magnitude = sum(x*x for x in axis) ** 0.5
            if axis_magnitude < 0.001:
                self.status_bar.showMessage("Invalid axis: cannot be zero vector")
                return
                
            self.opengl_widget.rotate_mesh(axis, angle)
            self.status_bar.showMessage(f"Applied rotation: {angle:.1f}° around ({axis[0]:.2f}, {axis[1]:.2f}, {axis[2]:.2f})")
            
        except ValueError:
            self.status_bar.showMessage("Invalid input values")

    def load_demo_car(self):
        """Load the demo car model"""
        import os
        demo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "obj", "Car.obj")
        if os.path.exists(demo_path):
            self.status_bar.showMessage("Loading demo car...")
            success = self.opengl_widget.load_mesh(demo_path)
            
            if success:
                if self.opengl_widget.mesh:
                    vertex_count = len(self.opengl_widget.mesh.vertices)
                    face_count = len(self.opengl_widget.mesh.faces)
                    self.object_info_label.setText(
                        f"Loaded: Car.obj (Demo)\n"
                        f"Vertices: {vertex_count:,}\n"
                        f"Faces: {face_count:,}"
                    )
                    self.status_bar.showMessage("Demo car loaded successfully")
            else:
                self.status_bar.showMessage("Failed to load demo car")
        else:
            self.status_bar.showMessage("Demo car file not found")

    def update_visualizations(self):
        """Update visualization settings in OpenGL widget"""
        self.opengl_widget.show_axes = self.show_axes_checkbox.isChecked()
        self.opengl_widget.show_rotation_axis = self.show_rotation_axis_checkbox.isChecked()
        self.opengl_widget.show_angle_label = self.show_angle_label_checkbox.isChecked()
        self.opengl_widget.show_original_object = self.show_original_checkbox.isChecked()
        self.opengl_widget.show_rotated_object = self.show_rotated_checkbox.isChecked()
        
        # Pass current rotation parameters to OpenGL widget
        if hasattr(self, 'axis_x_input'):
            axis = [
                self.axis_x_input.value(),
                self.axis_y_input.value(), 
                self.axis_z_input.value()
            ]
            angle = self.angle_input.value()
            self.opengl_widget.set_rotation_params(axis, angle)
        
        self.opengl_widget.update()
