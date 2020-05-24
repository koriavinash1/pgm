import sys
sys.path.append('..')

from pgm.helpers.misc import GenerateRandomGraph

graph = GenerateRandomGraph(10, type='BN', skeleton_only=True).Graph
graph.print(graph.rootNode)
