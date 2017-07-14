from SpaceToPlane import ConstructGraph, SpaceToPlane, visualize_result, output_result_to_file

G = ConstructGraph(filename="lines_40m.txt").G

res = SpaceToPlane(G)
res.run()

visualize_result(res)
output_result_to_file(res, "40m")