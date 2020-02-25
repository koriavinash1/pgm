import numpy as np
import pandas as pd
from collections import defaultdict


class Graph(object):
    """
        Adjancency list and Adjancency matrix 
        representation of the graph based on the input 

    """
    def __init__(self, type='list'):
        """
            type: captures the type of graph
                allowed values ['list', 'matrix']
        """
        self.type = type.lower()
        if self.type not in ['list', 'matrix']:
            raise ValueError("Invalid type found, allowed values are: ['list', 'matrix']")

        self.graph = {'node': defaultdict(list), 
                        'node_idx': defaultdict(list),
                        'node_weightage': defaultdict(list),
                        'edge': defaultdict(list), 
                        'edge_weightage': defaultdict(list)}


    def add_node(self, node, weightage=1):
        """
            adds node in the graph also helps in 
            assigning the weightage to each node

            node: can be ['int', 'str']
            weightage: ['int' or 'float']

        """
        node_idx = len(self.graph['nodes'])

        if not node in self.graph['nodes']:
            self.graph['node'].append(node)
            self.graph['node_weightage'].append(weightage)
            self.graph['node_idx'].append(node_idx)
            self.graph['edge'].append([])
            self.graph['edge_weightage'].append([])

        return node_idx


    def add_edges(self, nodeA, nodeB, edge_weightage=1, nodeA_weightage=1, nodeB_weightage=1):
        """
            adds a directed edge from nodeA to nodeB in 
            the graph also helps in assigning the weightage 
            to each edge

            nodeA -> nodeB

            nodeA: can be ['int', 'str']
            nodeB: can be ['int', 'str']
            nodeA_weightage: ['int' or 'float']
            nodeA_weightage: ['int' or 'float']
            edge_weightage: ['int' or 'float']
        """

        nodeA_idx = self.add_node(nodeA, nodeA_weightage)
        nodeB_idx = self.add_node(nodeB, nodeB_weightage)
        
        self.graph['edge'][nodeA_idx].append(nodeB_idx)
        self.graph['edge_weightage'][nodeA_idx].append(edge_weightage)


    def delete_edge(self, nodeA, nodeB):
        """
            deletes the directed edge from nodeA to nodeB

            function will remoce edge: nodeA -> nodeB


            nodeA: can be ['int', 'str']
            nodeB: can be ['int', 'str']
        """
        
        nodeA_idx = self.graph['node_idx'][self.graph['node'] == nodeA]
        nodeB_idx = self.graph['node_idx'][self.graph['node'] == nodeB]

        edge_idx  = np.where(self.graph['edge'][nodeA_idx] == nodeB_idx)
        self.graph['edge'][nodeA_idx].pop(edge_idx)
        self.graph['edge_weightage'][nodeA_idx].pop(edge_idx)


    def delete_node(self, node):
        """
            deletes the node from the graph
            also removes all the edges connecting to that specific node

            example:
                nodeA -> nodeB <- nodeC

            deleteing nodeB will remove
                edges:
                    nodeA -> nodeB
                    nodeC -> nodeB
                node:
                    nodeB


            node: can be ['int', 'str']
        """

        node_idx = np.where(self.graph['node_idx'][self.graph['node'] == node])
        node_idxs, edge_idxs = np.where(self.graph['edge'] == node_idx)

        for nidx, eidx in zip(node_idxs, edge_idxs):
            self.graph['edge'][nidx].pop(eidx)
            self.graph['edge_weightage'][nidx].pop(eidx)



