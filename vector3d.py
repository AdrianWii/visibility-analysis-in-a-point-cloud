import math

class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3D(x={self.x}, y={self.y}, z={self.z})"

    def normalize(self):
        distance = math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
        return Vector3D(self.x / distance, self.y / distance, self.z / distance)

    def cross_product(self, other):
        return Vector3D(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x
        )

    def scalar_product(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def __sub__(self, other):
        return Vector3D(self.x - other.x, self.y - other.y, self.z - other.z)