from operator import itemgetter
from Point import Point
import matplotlib.pyplot as plt
import json
from pprint import pprint


# TODO: 把"40m-plane-space.txt"这类文件改成json格式

# 需要以下几张对比图:
# 1. Rhino模型的线型和计算结果的对比图
# 2. Rhino模型转化为离散模型时缩短的距离
# 3. 有限元模型网格对模型的影响

class OdbData(object):
    def __init__(self, d: dict):
        self.boundPointsList: list = d["BoundPointsWithDeformation"]
        self.innerPointsList: list = d["Inner_Points"]
        self.sort()
        self.__init_dict()

    def sort(self):
        self.boundPointsList.sort(key=itemgetter(0, 1))
        self.innerPointsList.sort(key=itemgetter(0, 1))

    def __init_dict(self):
        self.__point_dict = dict()
        for tmp in self.boundPointsList + self.innerPointsList:
            p1 = Point(*tmp[:3])
            p2 = Point(*tmp[3:])
            self.__point_dict[p1] = p2

    @property
    def point_dict(self):
        return self.__point_dict


def load_odb(json_name: str) -> OdbData:
    assert json_name.endswith(".json")
    with open(json_name, "r") as f:
        d = json.load(f)
    for key in d:
        d[key] = eval(d[key])
    return OdbData(d)


def load_origin(origin_file: str) -> dict:
    out = dict()
    with open("40m-plane-space.txt", "r") as f:
        for line in f:
            raw1, raw2 = line.replace("), (", "|").strip("() \n").split("|")
            p1, p2 = Point.point_from_raw(raw1), Point.point_from_raw(raw2)
            out[p1] = p2
    return out


if __name__ == '__main__':
    odb = load_odb("40m-0-output-1000.json")
    odb2 = load_odb("40m-500-0-output-1000.json")
    odb3 = load_odb("40m-250-0-output-1000.json")

    origin_dict = load_origin("40m-plane-space.txt")

    mdb_xz, mdb_xx, mdb_zz = [], [], []
    odb_xx, odb_zz = [], []

    for key, val in odb.point_dict.items():
        assert isinstance(key, Point)
        # assert key in origin_dict
        if key.y == 0.0:
            mdb_p, odb_p = origin_dict[key], odb.point_dict[key]
            # plt.plot(mdb_p.x, mdb_p.z, "ro")
            mdb_xz.append((mdb_p.x, mdb_p.z))
            odb_xx.append(odb_p.x)
            odb_zz.append(odb_p.z)

    odb_xx2, odb_zz2 = [], []
    for key, val in odb2.point_dict.items():
        assert isinstance(key, Point)
        # assert key in origin_dict
        if key.y == 0.0:
            mdb_p, odb_p = origin_dict[key], odb2.point_dict[key]
            # plt.plot(mdb_p.x, mdb_p.z, "ro")
            # mdb_xz.append((mdb_p.x, mdb_p.z))
            odb_xx2.append(odb_p.x)
            odb_zz2.append(odb_p.z)

    odb_xx3, odb_zz3 = [], []
    for key, val in odb3.point_dict.items():
        assert isinstance(key, Point)
        # assert key in origin_dict
        if key.y == 0.0:
            odb_p = odb3.point_dict[key]
            # plt.plot(mdb_p.x, mdb_p.z, "ro")
            # mdb_xz.append((mdb_p.x, mdb_p.z))
            odb_xx3.append(odb_p.x)
            odb_zz3.append(odb_p.z)

    mdb_xz.sort(key=itemgetter(0, 1))
    for x, z in mdb_xz:
        mdb_xx.append(x)
        mdb_zz.append(z)
    plt.plot(mdb_xx, mdb_zz, "r-", label="origin-rhino-model")
    plt.plot(odb_xx, odb_zz, "bo", alpha=0.5, markersize=12, label="geo mesh: 1.0m")
    plt.plot(odb_xx2, odb_zz2, "k^", markersize=6, label="geo mesh: 0.5m")
    plt.plot(odb_xx3, odb_zz3, "ro", alpha=0.5, markersize=8, label="geo mesh: 0.25m")
    plt.legend(loc='upper left')
    plt.show()
