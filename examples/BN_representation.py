import sys
sys.path.append('..')
from pgm.representation.BN import Graph

G = Graph()


### one by one node addition and edge
G.add_node('A')
G.add_node('B')

G.add_edge('A', 'B')

print (G.graph)

### direct edge addition
G.add_edge('C', 'D')
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
