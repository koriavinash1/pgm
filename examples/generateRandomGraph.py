import sys
sys.path.append('..')

from pgm.helpers.misc import GenerateRandomGraph

graph = GenerateRandomGraph(20, type='MN').Graph
graph.print(graph.rootNode)