import numpy as np


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

        self.graph = {'node': [], 
                        'node_idx': [],
                        'edge': []} 


    def add_node(self, node):
        """
            adds node in the graph 

            node: can be ['int', 'str']

        """

        if not node in self.graph['node']:
            node_idx = len(self.graph['node']) 
            self.graph['node'].append(node)
            self.graph['node_idx'].append(node_idx)
            self.graph['edge'].append([])
        else:
            node_idx = self.graph['node_idx'][np.where(np.array(self.graph['node']) == node)[0][0]]
        return node_idx


    def add_edge(self, nodeA, nodeB):
        """
            adds a directed edge from nodeA to nodeB in 
            the graph also helps in assigning the weightage 
            to each edge

            nodeA -> nodeB

            nodeA: can be ['int', 'str']
            nodeB: can be ['int', 'str']
        """

        nodeA_idx = self.add_node(nodeA)
        nodeB_idx = self.add_node(nodeB)
        
        self.graph['edge'][nodeA_idx].append(nodeB_idx)


    def delete_edge(self, nodeA, nodeB):
        """
            deletes the directed edge from nodeA to nodeB

            function will remoce edge: nodeA -> nodeB


            nodeA: can be ['int', 'str']
            nodeB: can be ['int', 'str']
        """
        
        nodeA_idx = self.graph['node_idx'][np.where(np.array(self.graph['node']) == nodeA)[0][0]]
        nodeB_idx = self.graph['node_idx'][np.where(np.array(self.graph['node']) == nodeB)[0][0]]

        edge_idx  = np.where(np.array(self.graph['edge'][nodeA_idx]) == nodeB_idx)[0][0]
        self.graph['edge'][nodeA_idx].pop(edge_idx)


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

        node_idx = self.graph['node_idx'][np.where(np.array(self.graph['node']) == node)[0][0]]

        for nidx, eidxs in enumerate(self.graph['edge']):
        
            for j, eidx in enumerate(eidxs):
                if eidx == node_idx:
                    self.graph['edge'][nidx].pop(j)

            for j, eidx in enumerate(eidxs):
                if eidx > node_idx:
                    self.graph['edge'][nidx][j] =  self.graph['edge'][nidx][j] - 1


        for j in self.graph['node_idx'][node_idx + 1:]:
            self.graph['node_idx'][j] = j - 1

        self.graph['node'].pop(node_idx)
        self.graph['node_idx'].pop(node_idx)
        self.graph['edge'].pop(node_idx)
        

