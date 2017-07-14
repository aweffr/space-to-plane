from functools import total_ordering
from space_to_plane.Vector import Vector
from space_to_plane.Point import Point

@total_ordering
class Edge(object):
    def __init__(self, p1, p2, type=-1):
        self.p1 = p1
        self.p2 = p2
        self.vec = Vector(p1, p2)
        self.type = type
        self.length = self.vec.length

    def __str__(self):
        return str(self.p1) + "<---->" + str(self.p2)

    def __eq__(self, other):
        if self.p1 == other.p1 and self.p2 == other.p2:
            return True
        elif self.p1 == other.p2 and self.p2 == other.p1:
            return True
        else:
            return False

    def __lt__(self, other):
        assert isinstance(other, Edge)
        return self.vec.clock_angle < other.vec.clock_angle

    def __hash__(self):
        return hash(self.p1) + hash(self.p2)

    def get_point(self):
        return self.p1

    def other(self, p: Point) -> Point:
        if p == self.p1:
            return self.p2
        else:
            return self.p1

    def reverse(self):
        self.p1, self.p2 = self.p2, self.p1
        self.vec = Vector(self.p1, self.p2)

    @property
    def clock_angle(self):
        return self.vec.clock_angle
