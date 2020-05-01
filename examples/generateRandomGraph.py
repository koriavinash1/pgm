import sys
sys.path.append('..')

from pgm.helpers.misc import GenerateRandomGraph

graph = GenerateRandomGraph(100, type='MN').Graph
graph.print(graph.rootNode)