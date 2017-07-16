from operator import itemgetter
import json
from pprint import pprint

class OdbData(object):

    def __init__(self, d: dict):
        self.boundPointsList: list = d["BoundPointsWithDeformation"]
        self.innerPointsList: list = d["Inner_Points"]
        self.sort()

    def sort(self):
        self.boundPointsList.sort(key=itemgetter(0, 1))
        self.innerPointsList.sort(key=itemgetter(0, 1))

def load_odb(json_name: str) -> OdbData:
    assert json_name.endswith(".json")
    with open(json_name, "r") as f:
        d = json.load(f)
    for key in d:
        d[key] = eval(d[key])
    return OdbData(d)


if __name__ == '__main__':
    db = load_odb("40m-0-output.json")
    for p in db.boundPointsList:
        print(p)
    # print(db.boundPointsList)
