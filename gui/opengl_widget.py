from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QMouseEvent
from OpenGL.GL import *
from OpenGL.GLU import *
from graphics.mesh_object import MeshObject
from math3d.quaternion import Quaternion
from math3d.vector3d import Vector3D
import numpy as np

class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesh = None
        self.rotated_mesh = None
        
        # Camera controls
        self.camera_distance = 5.0
        self.camera_rotation_x = 0.0
        self.camera_rotation_y = 0.0
        self.last_mouse_pos = None
        
        # Object scaling
        self.scale_factor = 1.0
        
        # Visualization settings
        self.show_axes = True
        self.show_rotation_axis = True
        self.show_angle_label = True
        self.show_original_object = True
        self.show_rotated_object = True
        
        # Current rotation parameters
        self.current_rotation_axis = [1.0, 0.0, 0.0]
        self.current_rotation_angle = 45.0

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        
        # Set up lighting
        light_pos = [2.0, 2.0, 2.0, 1.0]
        light_ambient = [0.3, 0.3, 0.3, 1.0]
        light_diffuse = [0.8, 0.8, 0.8, 1.0]
        light_specular = [1.0, 1.0, 1.0, 1.0]
        
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
        glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
        glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
        glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
        
        glClearColor(0.1, 0.1, 0.1, 1)

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45, w / h if h != 0 else 1, 0.1, 100)

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        
        # Set up camera position based on mouse interaction
        glTranslatef(0, 0, -self.camera_distance)
        glRotatef(self.camera_rotation_x, 1, 0, 0)
        glRotatef(self.camera_rotation_y, 0, 1, 0)
        
        # Scale the object
        glScalef(self.scale_factor, self.scale_factor, self.scale_factor)

        # Draw visualizations
        if self.show_axes:
            self.draw_coordinate_axes()
        
        if self.show_rotation_axis:
            self.draw_rotation_axis()

        # Draw objects
        if self.mesh and self.show_original_object:
            glColor3f(0.8, 0.8, 0.9)  # Light blue: original mesh
            self.mesh.draw()
            
        if self.rotated_mesh and self.show_rotated_object:
            glColor3f(1.0, 0.3, 0.8)  # Magenta: rotated mesh
            self.rotated_mesh.draw()
            
        # Draw angle labels last (on top)
        if self.show_angle_label:
            self.draw_angle_labels()

    def load_mesh(self, filename):
        print(f"GLWidget: Loading mesh from {filename}")
        try:
            self.mesh = MeshObject(filename)
            self.rotated_mesh = None
            
            self.auto_scale_object()
            
            print(f"GLWidget: Mesh loaded successfully with {len(self.mesh.vertices)} vertices")
            self.update()
            return True
        except Exception as e:
            print(f"GLWidget: Error loading mesh: {e}")
            import traceback
            traceback.print_exc()
            return False

    def auto_scale_object(self):
        if self.mesh is None:
            return
            
        vertices = np.array(self.mesh.vertices)
        if len(vertices) == 0:
            return
            
        # Calculate bounding box
        min_coords = np.min(vertices, axis=0)
        max_coords = np.max(vertices, axis=0)
        size = max_coords - min_coords
        max_size = np.max(size)
        
        # Scale to fit roughly in a 2x2x2 box
        if max_size > 0:
            self.scale_factor = 2.0 / max_size
        else:
            self.scale_factor = 1.0

    def rotate_mesh(self, axis_input, angle_deg):
        if self.mesh is None:
            return

        self.current_rotation_axis = axis_input.copy()
        self.current_rotation_angle = angle_deg

        axis = Vector3D(*axis_input).normalize()
        angle_rad = angle_deg * 3.14159265 / 180

        from math import cos, sin
        w = cos(angle_rad / 2)
        vector_part = axis.normalize().mult(sin(angle_rad / 2))
        q = Quaternion(w, vector_part)

        # Rotate each vertex manually
        new_vertices = []
        for v in self.mesh.vertices:
            v_vec = Vector3D(*v)
            rotated_v = q.rotate(v_vec)
            new_vertices.append([rotated_v.x, rotated_v.y, rotated_v.z])

        self.rotated_mesh = self.mesh.create_copy_with_new_vertices(new_vertices)
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = event.pos()

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.last_mouse_pos is not None and event.buttons() & Qt.LeftButton:
            dx = event.x() - self.last_mouse_pos.x()
            dy = event.y() - self.last_mouse_pos.y()
            
            # Update camera rotation
            self.camera_rotation_y += dx * 0.5
            self.camera_rotation_x += dy * 0.5
            
            # Clamp vertical rotation
            self.camera_rotation_x = max(-90, min(90, self.camera_rotation_x))
            
            self.last_mouse_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.last_mouse_pos = None

    def wheelEvent(self, event):
        # Get wheel delta (positive = zoom in, negative = zoom out)
        delta = event.angleDelta().y()
        zoom_factor = 1.1 if delta > 0 else 0.9
        
        self.camera_distance *= zoom_factor
        self.camera_distance = max(0.5, min(50.0, self.camera_distance))  
        
        self.update()

    def reset_view(self):
        self.rotated_mesh = None
        self.camera_distance = 5.0
        self.camera_rotation_x = 0.0
        self.camera_rotation_y = 0.0
        # Reset rotation parameters
        self.current_rotation_axis = [1.0, 0.0, 0.0]
        self.current_rotation_angle = 45.0
        self.update()

    def set_rotation_params(self, axis, angle):
        self.current_rotation_axis = axis.copy()
        self.current_rotation_angle = angle

    def draw_coordinate_axes(self):
        glDisable(GL_LIGHTING)  # Disable lighting for axes
        glLineWidth(5.0)  # Thicker lines
        
        # Calculate appropriate axis length based on object size
        axis_length = 2.5
        if self.mesh is not None:
            vertices = np.array(self.mesh.vertices)
            if len(vertices) > 0:
                size = np.max(vertices, axis=0) - np.min(vertices, axis=0)
                max_size = np.max(size) * self.scale_factor
                axis_length = max(2.5, max_size * 1.5)  # Make axes longer than object
        
        glBegin(GL_LINES)
        
        # X axis - Red
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(axis_length, 0, 0)
        
        # Y axis - Green  
        glColor3f(0, 1, 0)
        glVertex3f(0, 0, 0)
        glVertex3f(0, axis_length, 0)
        
        # Z axis - Blue
        glColor3f(0, 0, 1)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, axis_length)
        
        glEnd()
        
        # Draw axis labels using simple geometry
        self.draw_axis_labels(axis_length)
        
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)  # Re-enable lighting

    def draw_axis_labels(self, axis_length):
        glColor3f(1, 1, 1)  # White color for labels
        glLineWidth(3.0)  # Thicker lines for labels
        
        label_offset = axis_length * 0.1  # Scale with axis length
        label_pos = axis_length + label_offset
        
        # X label (simple cross pattern)
        glBegin(GL_LINES)
        glVertex3f(label_pos - label_offset, -label_offset, 0)
        glVertex3f(label_pos + label_offset, label_offset, 0)
        glVertex3f(label_pos - label_offset, label_offset, 0)
        glVertex3f(label_pos + label_offset, -label_offset, 0)
        glEnd()
        
        # Y label (Y shape)
        glBegin(GL_LINES)
        glVertex3f(-label_offset, label_pos - label_offset, 0)
        glVertex3f(0, label_pos, 0)
        glVertex3f(label_offset, label_pos - label_offset, 0)
        glVertex3f(0, label_pos, 0)
        glVertex3f(0, label_pos, 0)
        glVertex3f(0, label_pos + label_offset, 0)
        glEnd()
        
        # Z label (Z shape)
        glBegin(GL_LINES)
        glVertex3f(-label_offset, 0, label_pos - label_offset)
        glVertex3f(label_offset, 0, label_pos - label_offset)
        glVertex3f(label_offset, 0, label_pos - label_offset)
        glVertex3f(-label_offset, 0, label_pos + label_offset)
        glVertex3f(-label_offset, 0, label_pos + label_offset)
        glVertex3f(label_offset, 0, label_pos + label_offset)
        glEnd()
        
        glLineWidth(1.0)

    def draw_rotation_axis(self):
        if not hasattr(self, 'current_rotation_axis'):
            return
            
        # Normalize the axis
        axis = np.array(self.current_rotation_axis)
        axis_length = np.linalg.norm(axis)
        if axis_length < 0.001:
            return
            
        axis = axis / axis_length
        
        glDisable(GL_LIGHTING)
        glLineWidth(6.0) 
        
        # Calculate appropriate scale based on object size
        scale = 3.0
        if self.mesh is not None:
            vertices = np.array(self.mesh.vertices)
            if len(vertices) > 0:
                size = np.max(vertices, axis=0) - np.min(vertices, axis=0)
                max_size = np.max(size) * self.scale_factor
                scale = max(3.0, max_size * 2.0)  # Make axis longer than object
        
        # Draw rotation axis as a bright yellow/orange line
        glColor3f(1.0, 0.8, 0.0)  # Yellow-orange
        glBegin(GL_LINES)
        
        # Draw line through origin in both directions
        glVertex3f(-axis[0] * scale, -axis[1] * scale, -axis[2] * scale)
        glVertex3f(axis[0] * scale, axis[1] * scale, axis[2] * scale)
        
        glEnd()
        
        # Draw arrow heads to show direction
        self.draw_arrow_heads(axis * scale)
        
        glLineWidth(1.0)
        glEnable(GL_LIGHTING)

    def draw_arrow_heads(self, end_point):
        arrow_size = 0.2
        
        # Calculate perpendicular vectors for arrow head
        axis = np.array([end_point[0], end_point[1], end_point[2]])
        axis = axis / np.linalg.norm(axis)
        
        # Find a perpendicular vector
        if abs(axis[0]) < 0.9:
            perp1 = np.array([1, 0, 0])
        else:
            perp1 = np.array([0, 1, 0])
            
        perp1 = perp1 - np.dot(perp1, axis) * axis
        perp1 = perp1 / np.linalg.norm(perp1)
        perp2 = np.cross(axis, perp1)
        
        glBegin(GL_LINES)
        
        # Arrow head lines
        for angle in [0, 90, 180, 270]:
            rad = np.radians(angle)
            offset = arrow_size * (perp1 * np.cos(rad) + perp2 * np.sin(rad))
            
            arrow_point = end_point - 0.3 * axis + offset
            glVertex3f(end_point[0], end_point[1], end_point[2])
            glVertex3f(arrow_point[0], arrow_point[1], arrow_point[2])
        
        glEnd()

    def draw_angle_labels(self):
        if not hasattr(self, 'current_rotation_angle') or not self.show_rotation_axis:
            return
            
        glDisable(GL_LIGHTING)
        glDisable(GL_DEPTH_TEST)  # Draw on top of everything
        
        # Get axis
        axis = np.array(self.current_rotation_axis)
        axis_length = np.linalg.norm(axis)
        if axis_length < 0.001:
            glEnable(GL_DEPTH_TEST)
            glEnable(GL_LIGHTING)
            return
            
        axis = axis / axis_length
        
        # Calculate appropriate scale and position
        scale = 1.5
        if self.mesh is not None:
            vertices = np.array(self.mesh.vertices)
            if len(vertices) > 0:
                size = np.max(vertices, axis=0) - np.min(vertices, axis=0)
                max_size = np.max(size) * self.scale_factor
                scale = max(1.5, max_size * 0.8)
        
        # Find position for angle display (offset from axis)
        if abs(axis[0]) < 0.9:
            perp = np.array([1, 0, 0])
        else:
            perp = np.array([0, 1, 0])
            
        perp = perp - np.dot(perp, axis) * axis
        perp = perp / np.linalg.norm(perp)
        
        # Create second perpendicular vector
        perp2 = np.cross(axis, perp)
        
        # Position the angle display 
        center_pos = axis * scale * 0.5  
        
        # Draw circular arc to show angle
        glColor3f(1.0, 1.0, 0.0)  
        glLineWidth(6.0) 
        
        import math
        angle_rad = math.radians(abs(self.current_rotation_angle))
        num_segments = max(12, int(abs(self.current_rotation_angle) / 5)) 
        radius = scale * 0.4  
        
        glBegin(GL_LINE_STRIP)
        for i in range(num_segments + 1):
            theta = angle_rad * (i / num_segments)
            if self.current_rotation_angle < 0:
                theta = -theta
            
            offset = radius * (perp * math.cos(theta) + perp2 * math.sin(theta))
            pos = center_pos + offset
            glVertex3f(pos[0], pos[1], pos[2])
        glEnd()
        
        text_pos = center_pos + perp * radius * 1.8 
        self.draw_angle_number(text_pos, self.current_rotation_angle)
        
        glPointSize(12.0) 
        glBegin(GL_POINTS)
        
        # Start point
        start_pos = center_pos + perp * radius
        glVertex3f(start_pos[0], start_pos[1], start_pos[2])
        
        # End point
        end_theta = angle_rad if self.current_rotation_angle >= 0 else -angle_rad
        end_offset = radius * (perp * math.cos(end_theta) + perp2 * math.sin(end_theta))
        end_pos = center_pos + end_offset
        glVertex3f(end_pos[0], end_pos[1], end_pos[2])
        
        glEnd()
        glPointSize(1.0)
        
        glLineWidth(1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHTING)

    def draw_angle_number(self, pos, angle):
        glColor3f(1.0, 1.0, 1.0)  
        glLineWidth(4.0) 
        
        glPointSize(40.0)  
        glColor3f(0.0, 0.0, 0.0)  # Black background
        glBegin(GL_POINTS)
        glVertex3f(pos[0], pos[1], pos[2])
        glEnd()
        
        glPointSize(35.0)
        glColor3f(0.2, 0.2, 0.2)  # Dark gray
        glBegin(GL_POINTS)
        glVertex3f(pos[0], pos[1], pos[2])
        glEnd()
        
        # Draw angle value with bright yellow color
        glColor3f(1.0, 1.0, 0.0) 
        
        # Convert angle to string and draw representation
        angle_str = f"{int(abs(angle))}"
        self.draw_simple_text(pos, angle_str)
        
        degree_pos = pos + np.array([len(angle_str) * 0.08, 0.05, 0])
        self.draw_degree_symbol(degree_pos)
        
        glPointSize(1.0)
        glLineWidth(1.0)

    def draw_simple_text(self, pos, text):
        glLineWidth(4.0)  
        char_width = 0.12  
        
        for i, char in enumerate(text):
            char_pos = pos + np.array([i * char_width - (len(text)-1) * char_width * 0.5, 0, 0])  # Center the text
            self.draw_simple_digit(char_pos, char)

    def draw_simple_digit(self, pos, digit):
        if not digit.isdigit():
            return
            
        d = int(digit)
        size = 0.08  
        
        # Define 7-segment display patterns
        segments = {
            0: [1,1,1,1,1,1,0],  # top, top-right, bottom-right, bottom, bottom-left, top-left, middle
            1: [0,1,1,0,0,0,0],
            2: [1,1,0,1,1,0,1],
            3: [1,1,1,1,0,0,1],
            4: [0,1,1,0,0,1,1],
            5: [1,0,1,1,0,1,1],
            6: [1,0,1,1,1,1,1],
            7: [1,1,1,0,0,0,0],
            8: [1,1,1,1,1,1,1],
            9: [1,1,1,1,0,1,1]
        }
        
        if d not in segments:
            return
            
        pattern = segments[d]
        
        glBegin(GL_LINES)
        
        # Top
        if pattern[0]:
            glVertex3f(pos[0] - size, pos[1] + size, pos[2])
            glVertex3f(pos[0] + size, pos[1] + size, pos[2])
            
        # Top-right
        if pattern[1]:
            glVertex3f(pos[0] + size, pos[1] + size, pos[2])
            glVertex3f(pos[0] + size, pos[1], pos[2])
            
        # Bottom-right
        if pattern[2]:
            glVertex3f(pos[0] + size, pos[1], pos[2])
            glVertex3f(pos[0] + size, pos[1] - size, pos[2])
            
        # Bottom
        if pattern[3]:
            glVertex3f(pos[0] + size, pos[1] - size, pos[2])
            glVertex3f(pos[0] - size, pos[1] - size, pos[2])
            
        # Bottom-left
        if pattern[4]:
            glVertex3f(pos[0] - size, pos[1] - size, pos[2])
            glVertex3f(pos[0] - size, pos[1], pos[2])
            
        # Top-left
        if pattern[5]:
            glVertex3f(pos[0] - size, pos[1], pos[2])
            glVertex3f(pos[0] - size, pos[1] + size, pos[2])
            
        # Middle
        if pattern[6]:
            glVertex3f(pos[0] - size, pos[1], pos[2])
            glVertex3f(pos[0] + size, pos[1], pos[2])
            
        glEnd()

    def draw_degree_symbol(self, pos):
        import math
        glBegin(GL_LINE_LOOP)
        radius = 0.03  
        for i in range(12):  
            angle = 2 * math.pi * i / 12
            x = pos[0] + radius * math.cos(angle)
            y = pos[1] + radius * math.sin(angle) + 0.05  
            glVertex3f(x, y, pos[2])
        glEnd()
