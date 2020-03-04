import numpy as np


class Graph(object):
    """
        Adjancency list and Adjancency matrix 
        representation of the graph based on the input 
    """
    def __init__(self, root):
        """
            root: node<object> or str
                if str it'll generate node and the following graph
        """
        self.nodesPresent = []

        if isinstance(root) == Node():
            self.rootNode = root
        elif isinstance(root) == str() or isinstance(root) == int():
            self.rootNode = Node()
            self.rootNode.name = root
        else:
            raise ValueError("Invalid type for root argument")


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
