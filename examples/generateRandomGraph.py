import sys
sys.path.append('..')

from pgm.helpers.misc import GenerateRandomGraph

graph = GenerateRandomGraph(5, type='BN').Graph
graph.print(graph.rootNode)