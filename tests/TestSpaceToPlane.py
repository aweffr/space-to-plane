import unittest
from space_to_plane.SpaceToPlane import SpaceToPlane
from space_to_plane.Point import Point
from space_to_plane.Edge import Edge


class TestSpaceToPlane(unittest.TestCase):
    def test_judge_vertical_edge_relation1(self):
        e1: Edge = Edge(Point(0, 0, 0), Point(0, 1, 0))
        e2: Edge = Edge(Point(0, 1, 0), Point(-6, -6, 0))

        self.assertEqual(SpaceToPlane.judge_vertical_edge_relation(e1, e2), -1)

    def test_judge_vertical_edge_relation2(self):
        e1: Edge = Edge(Point(0, 0, 0), Point(0, 1, 0))
        e2: Edge = Edge(Point(0, 1, 0), Point(0.99, 1, 0))

        self.assertEqual(SpaceToPlane.judge_vertical_edge_relation(e1, e2), 1)


if __name__ == '__main__':
    unittest.main()
