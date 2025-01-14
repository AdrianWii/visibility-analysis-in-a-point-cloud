from point3d import Point3D

class Face:
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
        self.centroid = self.compute_centroid()

    def compute_centroid(self):
        # Calculate the centroid as the average of the vertices
        x = (self.a.x + self.b.x + self.c.x) / 3
        y = (self.a.y + self.b.y + self.c.y) / 3
        z = (self.a.z + self.b.z + self.c.z) / 3
        return Point3D(x, y, z)

    def __repr__(self):
        return f"Face(a={self.a}, b={self.b}, c={self.c})"