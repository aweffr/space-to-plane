from functools import total_ordering

@total_ordering
class Point(object):
    def __init__(self, x, y, z=0.0):
        self.x, self.y, self.z = map(Point.strip_acc, [x, y, z])

    def __str__(self):
        return "(%.5f, %.5f, %.5f)" % (self.x, self.y, self.z)

    def __repr__(self):
        return "Point(%.5f, %.5f, %.5f)" % (self.x, self.y, self.z)

    def __eq__(self, other):
        assert isinstance(other, Point)
        if Point.abs_distance(self, other) < 0.00001:
            return True
        else:
            return False

    def __lt__(self, other):
        if 100000 * self.x + self.y < 100000 * other.x + other.y:
            return True
        else:
            return False

    def __hash__(self):
        return 0xffff * hash(self.x) + 0xff * hash(self.y) + hash(self.z)

    def __add__(self, other):
        x = self.x + other.dx
        y = self.y + other.dy
        z = self.z + other.dz
        return Point(x, y, z)

    @staticmethod
    def strip_acc(num):
        num = num + 0.0
        num = "%.5f" % num
        num = float(num)

        if abs(round(num) - num) < 0.00005:
            num = round(num)
        return num

    @staticmethod
    def parse_raw_data(s):
        s = list(map(float, s.split(",")))
        return s[0], s[1], s[2]

    @staticmethod
    def abs_distance(p1, p2):
        dis = abs(p1.x - p2.x) + abs(p1.y - p2.y) + abs(p1.z - p2.z)
        return dis

    @staticmethod
    def get_xy_plane_k(p1, p2):
        dx = p2.x - p1.x + 0.0
        dy = p2.y - p1.y + 0.0
        if abs(dx) < 0.0000001:
            if dx < 0:
                dx = -0.0000001
            else:
                dx = 0.0000001
        return dy / dx

    @staticmethod
    def clock_order(point_list) -> list:
        point_list = sorted(point_list)
        left_p = point_list[0]
        point_list = [left_p, ] + sorted(point_list[1:], key=lambda p: Point.get_xy_plane_k(left_p, p), reverse=True)
        return point_list
