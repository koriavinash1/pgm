import sys
sys.path.append('..')

from pgm.helpers.common import Node
from pgm.representation.LinkedListBN import Graph

rootNode = Node('rootNode')

graph = Graph(rootNode)
graph.add_node('node1', 'rootNode')
graph.add_node('node2', 'rootNode')
graph.add_node('node3', 'node1')
graph.add_edge('node2', 'node3')
graph.print(rootNode)

print("=="*10)


from pgm.helpers.trails import findTrails

ftrails = findTrails(rootNode, 'rootNode', 'node3')
print(ftrails.print())
