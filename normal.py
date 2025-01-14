
from point3d import Point3D
from vector3d import Vector3D
from typing import List

class Normal:
    def __init__(self, first: Point3D, second: Point3D, third: Point3D):
        self.first = first
        self.second = second
        self.third = third

    def vector(self, p1: Point3D, p2: Point3D):
        return Vector3D(p1.x - p2.x, p1.y - p2.y, p1.z - p2.z)

    def same_sign(self, num1, num2):
        return (num1 >= 0 and num2 >= 0) or (num1 < 0 and num2 < 0)

    def process(self, points: List[Point3D], light: Point3D):
        # Create vectors from the light point to the face vertices
        V = [self.vector(self.first, light), self.vector(self.second, light), self.vector(self.third, light)]
        normal = [V[0].cross_product(V[1]), V[0].cross_product(V[2]), V[1].cross_product(V[2])]
        scalar = [normal[0].scalar_product(V[2]), normal[1].scalar_product(V[1]), normal[2].scalar_product(V[0])]

        # Precompute side vectors and their normal
        side_vector1 = self.vector(self.second, self.first)
        side_vector2 = self.vector(self.third, self.first)
        side_normal = side_vector1.cross_product(side_vector2)

        scalar1 = side_normal.scalar_product(self.vector(light, self.first))

        for point in points:
            if point.mesh == 0 or point == self.first or point == self.second or point == self.third:
                continue

            point_vector = self.vector(point, light)
            cmp_scalar = [
                normal[0].scalar_product(point_vector),
                normal[1].scalar_product(point_vector),
                normal[2].scalar_product(point_vector)
            ]

            # Check if the point is inside the triangle
            if all(self.same_sign(s, c) for s, c in zip(scalar, cmp_scalar)):
                scalar2 = side_normal.scalar_product(self.vector(point, self.first))

                if not self.same_sign(scalar1, scalar2):
                    point.mesh = 0


    # def process(self, points: List[Point3D], light: Point3D):
    #     for point in points:
    #         if point.mesh == 0 or point == self.first or point == self.second or point == self.third:
    #             continue

    #         # Create vectors from the light point to the face vertices
    #         V = [self.vector(self.first, light), self.vector(self.second, light), self.vector(self.third, light)]

    #         # Calculate normals for each side of the triangle
    #         normal = [V[0].cross_product(V[1]), V[0].cross_product(V[2]), V[1].cross_product(V[2])]

    #         scalar = [normal[0].scalar_product(V[2]), normal[1].scalar_product(V[1]), normal[2].scalar_product(V[0])]
    #         cmp_scalar = [
    #             normal[0].scalar_product(self.vector(point, light)),
    #             normal[1].scalar_product(self.vector(point, light)),
    #             normal[2].scalar_product(self.vector(point, light))
    #         ]

    #         # Check if the point is inside the triangle
    #         if all(self.same_sign(s, c) for s, c in zip(scalar, cmp_scalar)):
    #             side_vector1 = self.vector(self.second, self.first)
    #             side_vector2 = self.vector(self.third, self.first)
    #             side_normal = side_vector1.cross_product(side_vector2)

    #             scalar1 = side_normal.scalar_product(self.vector(light, self.first))
    #             scalar2 = side_normal.scalar_product(self.vector(point, self.first))

    #             if not self.same_sign(scalar1, scalar2):
    #                 point.mesh = 0

    #     return points