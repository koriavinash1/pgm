import sys
sys.path.append('..')
from pgm.representation.BN import Graph

G = Graph()


### one by one node addition and edge
G.add_node('A', weightage=5)
G.add_node('B', weightage=10)

G.add_edges('A', 'B', edge_weightage=5)

print (G.graph)

### direct edge addition
G.add_edge('C', 'D', nodeA_weightage=5, nodeB_weightage=2, edge_weightage=10)
G.add_edge('B', 'C')
G.add_edge('A', 'C')
G.add_edge('A', 'D')
print (G.graph)

### delete edge
G.delete_edge('C', 'D')
print (G.graph)

### delete node
G.delete_node('C')
print (G.graph)
