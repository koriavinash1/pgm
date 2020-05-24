import numpy as np
from ..helpers.common import Node
from ..helpers.search import dfs

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

        if isinstance(root, Node):
            self.rootNode = root
        elif isinstance(root, str) or isinstance(root, int):
            self.rootNode = Node()
            self.rootNode.name = root
            self.rootNode.type = 'MN'
        else:
            raise ValueError("Invalid type for root argument")


    def add_node(self, node, nbrNodes):
        """
            adds node in the graph 
            node: can be ['int', 'str']
            nbrNodes: can be list(['int' or 'str'])
        """
        node = Node(node)
        node.type = 'MN'
        for nbrNode in nbrNodes:
            nbrNode = dfs(self.rootNode, nbrNode, type = 'MN').searchNode
            if nbrNode == -1:
                raise ValueError("nbrNode not found")
            node.nbrs.append(nbrNode)
            nbrNode.nbrs.append(node)


    def add_edge(self, node1, node2):
        """
            adds edge netween node1 and node2
            node1 -> node2
            node1: can be ['int', 'str']
            node2: can be ['int', 'str']
        """
        node1 = dfs(self.rootNode, node1, type = 'MN').searchNode
        node2 = dfs(self.rootNode, node2, type = 'MN').searchNode
        if (node1 == -1) or (node2 == -1):
            raise ValueError("Node1 or Node2 not found")

        if not node2 in node1.nbrs:
            node1.nbrs.append(node2)
        if not node1 in node2.nbrs:
            node2.nbrs.append(node1)


    def delete_edge(self, node1, node2):
        """
            removes edge between node1 and node2
            deletes node1->node2 edge

            node1: can be ['int', 'str']
            node2: can be ['int', 'str']
        """
        node1 = dfs(self.rootNode, node1, type = 'MN').searchNode
        node2 = dfs(self.rootNode, node2, type = 'MN').searchNode
        if (node1 == -1) or (node2 == -1):
            raise ValueError("Node1 or Node2 not found")
        
        for i, nbr in enumerate(node1.nbrs):
            if nbr.name == node2.name:
                node1.nbrs.pop(i)
                break

        for i, nbr in enumerate(node2.nbrs):
            if nbr.name == node1.name:
                node2.nbrs.pop(i)
                break
        return 


    def delete_node(self, node):
        """
            removes all the edges and node from the graph

            node: can be ['int', 'str']
        """
        node = dfs(self.rootNode, node, type = 'MN').searchNode

        if not (node == -1):
            raise ValueError ("Node doesn't exist")
        
        for i, nbr in enumerate(node.nbrs):
            for j, nnbr in enumerate(nbr.nbrs):
                if nnbr.name == node.name:
                    nbr.nbrs.pop(j)
                    break
            node.nbrs.pop(i)

        del node
        return


    def get_node(self, node):
        r""" search and returns the node

        node: can be ['int', 'str']
        """
        node = dfs(self.rootNode, node, type = 'MN').searchNode

        if (node == -1):
            raise ValueError("Node doesn't exist")
        self.current_node = node
        return node 


    def calculate_conditional(self, nodes, values):
        r""" calculates conditional distribution fixing the
        values of given nodes

        nodes: can be list of ['int', 'str' or Node object]
        values: [node_value in same order]
        """

        raise NotImplementedError()


    def calculate_marginals(self, nodes):
        r""" removes the node and restimates marginals

        nodes: can be list of ['int', 'str' or Node object]
        """

        raise NotImplementedError()


    def print(self, node):
        if node == None:
            return

        queue = [node]
        visited = []
        for node in queue:

            if not node.name in visited:
                print("node: {}, nbrs: {}".format(node.name, 
                                                [nd.name for nd in node.nbrs]))
                queue.extend(node.nbrs)            
                visited.append(node.name)
