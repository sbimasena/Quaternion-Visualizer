class Vector3D:
    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3D({self.x}, {self.y}, {self.z})"

    def normalize(self):
        length = (self.x**2 + self.y**2 + self.z**2) ** 0.5
        if length == 0:
            return Vector3D(0, 0, 0)
        return Vector3D(self.x / length, self.y / length, self.z / length)
    
    def cross(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )
    
    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z
    
    def mult(self, scalar):
        return Vector3D(self.x * scalar, self.y * scalar, self.z * scalar)

    def round(self, epsilon=1e-12):
        clean_x = 0.0 if abs(self.x) < epsilon else self.x
        clean_y = 0.0 if abs(self.y) < epsilon else self.y
        clean_z = 0.0 if abs(self.z) < epsilon else self.z
        return Vector3D(clean_x, clean_y, clean_z)