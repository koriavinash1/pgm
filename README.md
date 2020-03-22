# PGM
[![Build Status](https://travis-ci.org/koriavinash1/pgm.svg?branch=master)](https://travis-ci.org/koriavinash1/pgm)
[![PyPI version](https://badge.fury.io/py/ppgm.svg)](https://badge.fury.io/py/ppgm)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Probabilistic graphs: Representation, Learning, and Inference

# Features

- [x] Representation
  - [x] Bayesian Network Representation
  - [x] Linked List BN Representation
  - [x] Linked List MN Representation
- [x] Inference
  - [x] Metropolis-Hastings algorithm
  - [x] Gibbs Sampling on 2d grid
  - [ ] Generalized Gibbs Sampling
  - [ ] Message Parsing and BP
  - [ ] VE
  - [ ] Causal Interventions
- [x] search methods
  - [x] DFS
  - [x] BFS
- [x] Additional
  - [x] Finding Active Trails
- [ ] Learning 
  
# Usage
Check examples to understand all routines

### LinkedList BN representation
```
from pgm.helpers.common import Node
from pgm.representation.LinkedListBN import Graph

rootNode = Node('rootNode')

graph = Graph(rootNode)
graph.add_node('node1', 'rootNode')
graph.add_node('node2', 'rootNode')
graph.add_node('node3', 'node1')
graph.add_edge('node2', 'node3')
graph.print(rootNode)

# =============== OUTPUT ===============
node: rootNode, children: ['node1', 'node2'], parents: []
node: node1, children: ['node3'], parents: ['rootNode']
node: node2, children: ['node3'], parents: ['rootNode']
node: node3, children: [], parents: ['node1', 'node2']
```

### Search dfs
```
from pgm.helpers.search import dfs

root = rootNode
searchNode = 'node4'
node = dfs(root, searchNode)
```

### GetTrails for above BN
```
from pgm.helpers.common import Node
from pgm.representation.LinkedListBN import Graph

rootNode = Node('rootNode')

graph = Graph(rootNode)
graph.add_node('node1', 'rootNode')
graph.add_node('node2', 'rootNode')
graph.add_node('node3', 'node1')
graph.add_edge('node2', 'node3')

from pgm.helpers.trails import findTrails

ftrails = findTrails(rootNode, 'rootNode', 'node3')
print(ftrails.print())

# =============== OUTPUT ===============
[['rootNode', 'node1', 'node3'], ['rootNode', 'node2', 'node3']]
```

# Contact
- Avinash Kori (koriavinash1@gmail.com)
