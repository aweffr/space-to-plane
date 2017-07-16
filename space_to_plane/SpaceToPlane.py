from collections import defaultdict, deque
from space_to_plane.Vector import Vector
from space_to_plane.Edge import Edge
from space_to_plane.Point import Point
from copy import deepcopy
import matplotlib.pyplot as plt
from random import random

# CONST
INF = 0x7fffffff


def is_int(num):
    return abs(num - round(num)) <= 0.0001


def get_left_most_point(point_map: dict):
    """Get the most left point which both x and y are integer."""
    left_most_point = Point(INF, INF, 0)
    for point_space, point_plane in point_map.items():
        print("In get_left_most_point(),", point_plane.x)
        if is_int(point_plane.x) and is_int(point_plane.y) and point_plane.x < left_most_point.x:
            left_most_point = point_plane
    return left_most_point


class ConstructGraph(object):
    def __init__(self, filename):
        raw_data = []

        # Example line of file:
        # (19.58137512207,-1.015897435618E-16,9.806725502014), (19.6015434265137,0.996934771537781,9.73113346099854)
        with open(filename, "r") as f:
            for line in f:
                line = line.strip()
                line = line.replace("), (", "|").replace("(", "").replace(")", "")
                line = line.split("|")
                raw_data.append(line)

        G = defaultdict(set)

        for raw1, raw2 in raw_data:
            p1 = Point(*Point.parse_raw_data(raw1))
            p2 = Point(*Point.parse_raw_data(raw2))
            e = Edge(p1, p2)
            G[p1].add(e)
            G[p2].add(e)

        self.G = G


class SpaceToPlane(object):
    def __init__(self, G):
        assert isinstance(G, defaultdict)
        self.G = G
        self.edgeList = self.__get_all_edges()
        self.pointList = self.__get_all_points()
        self.parent_edge: dict = None
        self.spaceToPlane: dict = dict()  # solution_result

    def __get_all_edges(self):
        out = set()
        for edges in self.G.values():
            out.update(edges)
        return list(out)

    def __get_all_points(self):
        out = deque(self.G.keys())
        return out

    @staticmethod
    def get_z_max_point(point_list):
        """O(n), get the point of z_max in list"""
        assert len(point_list) > 0, "point_list should not be empty!"
        out = point_list[0]
        assert isinstance(out, Point)
        for tmp in point_list:
            assert isinstance(tmp, Point)
            if tmp.z > out.z:
                out = tmp
        return out

    @staticmethod
    def judge_vertical_edge_relation(e1: Edge, e2: Edge):
        """determine relationship between e1 and e2, output +1 or -1"""
        cnt = 0
        ang1 = e1.clock_angle
        ang2 = e2.clock_angle
        if ang2 < ang1:
            ang2 += 360
        while ang1 + (cnt + 30) < ang2:
            cnt += 30
        if cnt < 180:
            return 1
        else:
            return -1

    @staticmethod
    def copy_and_sort(center_point: Point, around_edges_list: list) -> list:
        """
        当around_edges_list中的Edge对象的p1不是center_point时, 调整Edge中两个点的顺序
        :param center_point: 
        :param around_edges_list: 
        :return: 
        """
        out = deepcopy(around_edges_list)
        for edge in out:
            assert isinstance(edge, Edge)
            if edge.p1 != center_point:
                edge.reverse()
        out = sorted(out)
        return out

    @staticmethod
    def get_next_point(from_point: Point, edge: Edge) -> Point:
        """Input the current plane point and next edge, get the next point on plane"""
        assert from_point.z == 0, "Input Point should be on plane!(z == 0)"
        length = edge.length
        if abs(length - 0.25) < 0.001:
            length = 0.25
        if abs(length - 0.5) < 0.001:
            length = 0.5
        if abs(length - 1.0) < 0.001:
            length = 1.0
        if edge.type == 0:
            to_point = from_point + Vector.North(length)
        elif edge.type == 1:
            to_point = from_point + Vector.East(length)
        elif edge.type == 2:
            to_point = from_point + Vector.South(length)
        elif edge.type == 3:
            to_point = from_point + Vector.West(length)
        else:
            raise Exception("Input Edge's type is wrong!")
        return to_point

    def run(self) -> bool:
        # 取第一个点，将其相邻四个边按顺时针排序，标记0, 1, 2, 3
        start_point = self.get_z_max_point(self.pointList)
        around_edges = self.G[start_point]
        if len(around_edges) != 4:
            raise Exception("Error at `start_point`: start_point needs 4 around_edges!")
        copied_around_edges = self.copy_and_sort(start_point, around_edges)

        # When ordered by clock_angle, if the first edge's angle is above 45 degree,
        # we choose the north-west edge as the `0 edge`.
        if Vector.plane_angle(Vector.North(), copied_around_edges[0].vec, degree=True) > 45:
            offset = 1
        else:
            offset = 0

        self.spaceToPlane[start_point] = Point(0.0, 0.0, 0.0)

        # parent_edge: record where the current point is from.
        # point_queue: like prim's algorithm, point in this queue is the border of current expanding graph.
        parent_edge = dict()
        point_queue = deque()

        for idx, copied_edge in enumerate(copied_around_edges):
            assert isinstance(copied_edge, Edge)
            p1 = copied_edge.p1
            p2 = copied_edge.other(p1)

            point_queue.append(p2)
            copied_edge.type = (idx + offset + 4) % 4
            for edge in around_edges:
                if edge == copied_edge:
                    edge.type = copied_edge.type
            parent_edge[p2] = copied_edge

            assert p1 == start_point, "In this loop, center point should be the  first point!"

            p1_on_plane = self.spaceToPlane[p1]
            p2_on_plane = self.get_next_point(p1_on_plane, copied_edge)
            self.spaceToPlane[p2] = p2_on_plane

        # start of main loop
        while len(point_queue) > 0:
            p1 = point_queue.popleft()
            from_edge: Edge = parent_edge[p1]
            from_point = from_edge.other(p1)

            # from_edge's p2 should be current `center point`
            if from_edge.p2 != p1:
                from_edge.reverse()
            assert from_edge.p2 == p1

            from_vector = Vector(from_point, p1, need_regular=True)

            around_edges = self.G[p1]
            copied_around_edges = self.copy_and_sort(p1, around_edges)

            # There are three types in the around_edges:
            # 1. The edge where current point come from.
            # 2. Parallel to the from_edge, should have the same direction on the plane.
            # 3. Vertical to the from_edge, shoud determine it's type:
            #        eg: if from_edge's type is 1, vertical edge should be 0 or 2.

            vertical_edges = []

            for copied_edge in copied_around_edges:
                if copied_edge == from_edge:
                    continue
                if copied_edge.vec.length < 0.0001 or from_vector.length < 0.0001:
                    continue
                elif Vector.space_angle(copied_edge.vec, from_vector, degree=True) > 45:
                    vertical_edges.append(copied_edge)
                else:  # angle <= 45
                    next_edge = copied_edge
                    p2 = copied_edge.other(p1)
                    parent_edge[p2] = next_edge
                    point_queue.append(p2)
                    next_edge.type = from_edge.type  # extend
                    p1_on_plane = self.spaceToPlane[p1]
                    p2_on_plane = self.get_next_point(from_point=p1_on_plane,
                                                      edge=next_edge)
                    self.spaceToPlane[p2] = p2_on_plane

            # if next_edge is not None:

            for vertical_edge in vertical_edges:
                if vertical_edge.type != -1:
                    continue
                else:
                    assert from_edge.p2 == vertical_edge.p1
                    diff = self.judge_vertical_edge_relation(from_edge, vertical_edge)
                    relation_type = (from_edge.type + diff + 4) % 4
                    for edge in around_edges:
                        if edge == vertical_edge:
                            edge.type = relation_type
                            p2 = edge.other(p1)
                            point_queue.append(p2)
                            parent_edge[p2] = edge
                            p1_on_plane = self.spaceToPlane[p1]
                            p2_on_plane = self.get_next_point(from_point=p1_on_plane,
                                                              edge=edge)
                            self.spaceToPlane[p2] = p2_on_plane
        # End of main loop
        self.parent_edge = parent_edge
        return True


def visualize_result(res: SpaceToPlane, *plot_args, **plot_kwargs):
    left_most_point = get_left_most_point(res.spaceToPlane)
    print("left_most_point=%r" % left_most_point)
    offset_vector = Vector(left_most_point, Point(1, 0, 0))
    print("Move %r to %r" % (left_most_point, Point(1, 0, 0)), "offset", offset_vector)

    xx = []
    yy = []
    for key in res.spaceToPlane.keys():
        point_plane = res.spaceToPlane[key]
        new_point_plane = point_plane + offset_vector
        res.spaceToPlane[key] = new_point_plane
        xx.append(new_point_plane.x)
        yy.append(new_point_plane.y)
        # plt.plot(new_point_plane.x, new_point_plane.y, *plot_args, **plot_kwargs)
    plt.plot(xx, yy, *plot_args, **plot_kwargs)
    plt.show()


def output_result_to_file(res: SpaceToPlane, filename):
    with open("{filename}-plane-space.txt".format(filename=filename), "w") as f:
        for space_point, plane_point in res.spaceToPlane.items():
            f.writelines(str(plane_point) + ", " + str(space_point) + "\n")

    with open("{filename}-plane-points.txt".format(filename=filename), "w") as f:
        for plane_point in sorted(res.spaceToPlane.values()):
            f.writelines(str(plane_point) + "\n")
    print("write finish")
