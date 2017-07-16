from SpaceToPlane import ConstructGraph, SpaceToPlane, visualize_result, output_result_to_file
import matplotlib.pyplot as plt

if __name__ == '__main__':
    G = ConstructGraph(filename="lines_40m-250.txt").G

    res: SpaceToPlane = SpaceToPlane(G)
    res.run()

    # for p in res.spaceToPlane.values():
    #     plt.plot(p.x, p.y, "o")
    # plt.show()

    visualize_result(res, "k.", alpha=0.6, markersize=0.5)
    output_result_to_file(res, "40m-250")
