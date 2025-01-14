class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.mesh = 1 # 1 visible, 0 hidden

    def __repr__(self):
        return f"Point3D(x={self.x}, y={self.y}, z={self.z})"
    
    def __eq__(self, other):
        # Check if another object is equal to this one
        if not isinstance(other, Point3D):
            return NotImplemented
        return self.x == other.x and self.y == other.y and self.z == other.z
    
    def distance(self, other):
        # Calculate squared distance to another Point3D
        dx = self.x - other.x
        dy = self.y - other.y
        dz = self.z - other.z
        return dx * dx + dy * dy + dz * dz