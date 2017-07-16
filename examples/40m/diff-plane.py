# coding=utf-8
import json
import matplotlib.pyplot as plt


def get_xx_yy_from_mdb(mdb: dict) -> (list, list):
    xx, yy = [], []
    for p1, p2 in mdb["xCoordPoints"] + mdb["yCoordPoints"]:
        xx.extend([p1[0], p2[0]])
        yy.extend([p1[1], p2[1]])
    return xx, yy


if __name__ == '__main__':
    f1 = open("40m-0.json")
    f2 = open("40m-500-0.json")
    f3 = open("40m-250-0.json")

    p1, p2, p3 = None, None, None
    try:
        p1 = json.load(f1)
        p2 = json.load(f2)
        p3 = json.load(f3)
    except Exception as e:
        print("Read fail exception=", e)
    finally:
        f1.close()
        f2.close()
        f3.close()
    print(p1.keys())

    xx1, yy1 = get_xx_yy_from_mdb(p1)
    xx2, yy2 = get_xx_yy_from_mdb(p2)
    xx3, yy3 = get_xx_yy_from_mdb(p3)
    plt.plot(xx1, yy1, "ro", alpha=0.5, markersize=8, label="geo mesh: 1.0m")
    plt.plot(xx2, yy2, "b^", alpha=0.5, markersize=8, label="geo mesh: 0.5m")
    plt.plot(xx3, yy3, "ko", alpha=0.5, markersize=8, label="geo mesh: 0.25m")
    plt.legend(loc='upper left')
    plt.show()
