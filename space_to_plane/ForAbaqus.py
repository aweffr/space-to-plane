# coding=utf-8
"""
Generate proper format for Abaqus modeling.
Should be run only on Python2.7.
"""

from operator import itemgetter
from collections import defaultdict
from pprint import pprint
from math import floor, ceil
import shelve
import json

point_list = []


def is_int(num):
    return abs(num - round(num)) <= 0.0001


def eliminate_inner_points(d, opt):
    """
    :param d: dict
    eliminate those points that is not integer inside plane gridshell.
    """
    for key in d:
        tmp1 = sorted(d[key], key=itemgetter(0, 1))
        tmp2 = []
        for idx, point in enumerate(tmp1):
            if idx == 0 or idx == (len(tmp1) - 1):
                tmp2.append(point)
            else:
                if opt == "x":
                    if is_int(point[1]):
                        tmp2.append(point)
                elif opt == "y":
                    if is_int(point[0]):
                        tmp2.append(point)
        diff = len(tmp1) - len(tmp2)
        print("%d points has been eliminated! in %s_dict" % (diff, opt))
        d[key] = tmp2


def read_from_point_file(filename):
    x_dict = defaultdict(list)
    y_dict = defaultdict(list)

    with open(filename, "r") as f:
        for line in f:
            line = line.strip("() \n").split(",")
            point = list(map(float, line))
            for idx, val in enumerate(point):
                if is_int(val):
                    point[idx] = round(val)
            if is_int(point[0]):
                x_dict[point[0]].append(point[:])
            if is_int(point[1]):
                y_dict[point[1]].append(point[:])

    # For mesh=0.25m's condition, we just need the integer inner node.
    eliminate_inner_points(x_dict, "x")
    eliminate_inner_points(y_dict, "y")

    return x_dict, y_dict


# -----------生成给abaqus建模的脚本的数据格式----------------

def split(point_list):
    status = [[point, False] for point in point_list]
    status[0][1] = True
    status[-1][1] = True
    for idx in range(len(point_list) - 1):
        p1, p2 = point_list[idx], point_list[idx + 1]
        if abs(p1[0] - p2[0]) + abs(p1[1] - p2[1]) > 1.0:
            status[idx][1] = True
            status[idx + 1][1] = True
    tmp_2D, tmp_3D, in_tmp = [], [], []
    for point, is_bound in status:
        if is_bound:
            tmp_2D.append(point[:-1])
            tmp_3D.append(point)
        else:
            in_tmp.append(point)
        if len(tmp_2D) == 2:
            yield tmp_2D[:], tmp_3D[:], in_tmp[:]
            tmp_2D, tmp_3D, in_tmp = [], [], []


def main(point_file, abaqus_file):
    assert isinstance(point_file, str) and isinstance(abaqus_file, str)
    assert point_file.endswith(".txt") and abaqus_file.endswith(".dat"), \
        "invalid file name, %s, %s" % (point_file, abaqus_file)

    x_dict, y_dict = read_from_point_file(point_file)

    xBoundPoints = []
    yBoundPoints = []
    inCoordPoints = []
    xCoordPoints_3D = []
    yCoordPoints_3D = []
    inCoordPoints_3D = []
    vector = (0, 0, 0)

    for point_list in x_dict.values():
        # tmp_2D = [point_list[0][:-1], point_list[-1][:-1]]
        # tmp_3D = [point_list[0], point_list[-1]]
        for tmp_2D, tmp_3D, in_tmp in split(point_list):
            xBoundPoints.append(tmp_2D)
            xCoordPoints_3D.extend(tmp_3D)
            for p in in_tmp:
                if abs(p[1]) == 12.0:
                    continue
                inCoordPoints.append(p)
                inCoordPoints_3D.append(p)

    for point_list in y_dict.values():
        # tmp_2D = [point_list[0][:-1], point_list[-1][:-1]]
        # tmp_3D = [point_list[0], point_list[-1]]
        for tmp_2D, tmp_3D, in_tmp in split(point_list):
            if abs(tmp_2D[0][1]) == 12.0:
                continue
            yBoundPoints.append(tmp_2D)
            yCoordPoints_3D.extend(tmp_3D)

    f = shelve.open(abaqus_file)
    try:
        f['mdbSaveName'] = abaqus_file.replace(".dat", "-mdb")
        f['odbSaveName'] = abaqus_file.replace(".dat", "-odb")
        f["time"] = 0

        f["xCoordPoints"] = xBoundPoints
        f["yCoordPoints"] = yBoundPoints
        f["inCoordPoints"] = inCoordPoints
        f["xCoordPoints_3D"] = xCoordPoints_3D
        f["yCoordPoints_3D"] = yCoordPoints_3D
        f["inCoordPoints_3D"] = inCoordPoints_3D
        f["vector"] = vector

        d = dict(f)
        with open(abaqus_file.replace(".dat", ".json"), "w") as json_file:
            json_file.writelines(json.dumps(d) + "\n")
    except Exception as e:
        print("write output files failed. Exception:\n", e)
    finally:
        f.close()


if __name__ == '__main__':
    import os

    path_1 = "C:/Users/aweff/PycharmProjects/space-to-plane/examples/40m"
    path_2 = "E:/SpaceToPlane/examples/40m"

    os.chdir(path_1)
    main("40m-250-plane-points.txt", "40m-250-0.dat")
