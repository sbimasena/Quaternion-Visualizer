from math3d.vector3d import Vector3D

class Quaternion:
    def __init__(self, w=1.0, vector: Vector3D = None):
        self.w = w
        if vector is not None:
            self.vector = vector
        else:
            self.vector = Vector3D(0.0, 0.0, 0.0)
    
    @property
    def x(self):
        return self.vector.x
    
    @property
    def y(self):
        return self.vector.y
    
    @property
    def z(self):
        return self.vector.z
    
    @x.setter
    def x(self, value):
        self.vector.x = value
    
    @y.setter
    def y(self, value):
        self.vector.y = value
    
    @z.setter
    def z(self, value):
        self.vector.z = value

    def __repr__(self):
        x_part = f"{'+' if self.x >= 0 else ''}{self.x}i" if self.x != 0 else ""
        y_part = f"{'+' if self.y >= 0 else ''}{self.y}j" if self.y != 0 else ""
        z_part = f"{'+' if self.z >= 0 else ''}{self.z}k" if self.z != 0 else ""
        
        result = str(self.w)
        
        for part in [x_part, y_part, z_part]:
            if part:
                if result and not part.startswith('-'):
                    result += "" + part
                else:
                    result += part
        
        return result

    def __add__(self, other):
        result_vector = Vector3D(self.x + other.x, self.y + other.y, self.z + other.z)
        return Quaternion(self.w + other.w, result_vector)

    def __sub__(self, other):
        result_vector = Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)
        return Quaternion(self.w - other.w, result_vector)

    def __mul__(self, other):
        if isinstance(other, Quaternion):
            w = (self.w * other.w - self.x * other.x - self.y * other.y - self.z * other.z)
            x = (self.w * other.x + self.x * other.w + self.y * other.z - self.z * other.y)
            y = (self.w * other.y - self.x * other.z + self.y * other.w + self.z * other.x)
            z = (self.w * other.z + self.x * other.y - self.y * other.x + self.z * other.w)
            result_vector = Vector3D(x, y, z)
            return Quaternion(w, result_vector)
        else:
            raise TypeError("Multiplication is only supported with another Quaternion.")
    
    def conjugate(self):
        conjugated_vector = Vector3D(-self.x, -self.y, -self.z)
        return Quaternion(self.w, conjugated_vector)

    def rotate(self, vector: Vector3D):
        q_vector = Quaternion(0, vector)
        rotated_vector = self * q_vector * self.conjugate()
        result = Vector3D(rotated_vector.x, rotated_vector.y, rotated_vector.z)
        return result