import sys
sys.path.append('..')

from pgm.helpers.common import Node
from pgm.representation.LinkedListBN import Graph

rootNode = Node('rootNode')
rootNode.values = [0,1,2]
rootNode.set_distribution()


graph = Graph(rootNode)
graph.add_node('node1', 'rootNode')
graph.print(rootNode)

node1 = graph.get_node('node1')
node1.values=[1, 2, 3]
node1.set_distribution()