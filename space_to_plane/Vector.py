from .Point import Point
from math import sqrt, acos, pi


def is_number(obj):
    return isinstance(obj, int) or isinstance(obj, float)


class Vector(object):
    def __init__(self, p1, p2, p3=0.0, need_regular=False):
        if isinstance(p1, Point) and isinstance(p2, Point):
            self.dx = p2.x - p1.x
            self.dy = p2.y - p1.y
            self.dz = p2.z - p1.z

        elif is_number(p1) and is_number(p2) and is_number(p3):
            self.dx = p1 + 0.0
            self.dy = p2 + 0.0
            self.dz = p3 + 0.0

        if need_regular:
            self.regularization()

        self.length = sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)
        if abs(self.length - 1.0) < 0.00001:
            self.length = 1.0

        self.clock_angle = Vector.clock_plane_angle(self)

    def regularization(self):
        assert abs(self.dx) + abs(self.dy) + abs(self.dz) > 0.00001
        r = sqrt(self.dx ** 2 + self.dy ** 2 + self.dz ** 2)
        self.dx /= r
        self.dy /= r
        self.dz /= r

    def __str__(self):
        return "(%.5f, %.5f, %.5f)" % (self.dx, self.dy, self.dz)

    @staticmethod
    def space_angle(vector1, vector2, degree=False):
        x1, y1, z1 = vector1.dx, vector1.dy, vector1.dz
        x2, y2, z2 = vector2.dx, vector2.dy, vector2.dz
        cos_value = (x1 * x2 + y1 * y2 + z1 * z2) / (
            sqrt(x1 * x1 + y1 * y1 + z1 * z1) * sqrt(x2 * x2 + y2 * y2 + z2 * z2))
        rad = acos(cos_value)
        if degree:
            return 180 / pi * rad
        else:
            return rad

    @staticmethod
    def plane_angle(vector1, vector2, degree=False):
        x1, y1 = vector1.dx, vector1.dy
        x2, y2 = vector2.dx, vector2.dy
        cos_value = (x1 * x2 + y1 * y2) / (sqrt(x1 * x1 + y1 * y1) * sqrt(x2 * x2 + y2 * y2))
        rad = acos(cos_value)
        if degree:
            return 180 / pi * rad
        else:
            return rad

    @staticmethod
    def North(length=1.0):
        return Vector(Point(0.0, 0.0), Point(0.0, length))

    @staticmethod
    def East(length=1.0):
        return Vector(Point(0.0, 0.0), Point(length, 0.0))

    @staticmethod
    def South(length=1.0):
        return Vector(Point(0.0, 0.0), Point(0.0, -length))

    @staticmethod
    def West(length=1.0):
        return Vector(Point(0.0, 0.0), Point(-length, 0.0))

    @staticmethod
    def clock_plane_angle(vector):
        assert isinstance(vector, Vector)
        dx, dy = vector.dx, vector.dy
        if dx == 0.0 and dy > 0:
            return 0.0
        elif dx > 0 and dy > 0:
            return 0.0 + abs(Vector.plane_angle(Vector.North(), vector, degree=True))
        elif dx > 0 and dy == 0:
            return 90.0
        elif dx > 0 and dy < 0:
            return 90.0 + + abs(Vector.plane_angle(Vector.East(), vector, degree=True))
        elif dx == 0 and dy < 0:
            return 180.0
        elif dx < 0 and dy < 0:
            return 180.0 + abs(Vector.plane_angle(Vector.South(), vector, degree=True))
        elif dx < 0 and dy == 0:
            return 270.0
        elif dx < 0 and dy > 0:
            return 270 + abs(Vector.plane_angle(Vector.West(), vector, degree=True))
        elif dx == 0.0 and dy == 0.0:
            return 0.0
        else:
            raise Exception("Wrong at clock_plane_angle( " + str(vector) + " )")
