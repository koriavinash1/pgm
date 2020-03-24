import numpy as np
from ..helpers.common import MNNode as Node
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
        else:
            raise ValueError("Invalid type for root argument")


    def add_node(self, node, nbrNodes):
        """
            adds node in the graph 
            node: can be ['int', 'str']
            nbrNodes: can be list(['int' or 'str'])
        """
        node = Node(node)
        for nbrNode in nbrNodes:
            nbrNode = dfs(self.rootNode, nbrNode).searchNode
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
        node1 = dfs(self.rootNode, node1).searchNode
        node2 = dfs(self.rootNode, node2).searchNode
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
        node1 = dfs(self.rootNode, node1).searchNode
        node2 = dfs(self.rootNode, node2).searchNode
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
        node = dfs(self.rootNode, node).searchNode

        if not (node == -1):
            pass

        pass


    def print(self, node):
        if node == None:
            return

        queue = [node]
        visited = []
        for node in queue:

            if not node.name in visited:
                print("node: {}, nbrs: {}".format(node.name, 
                                                [nd.name for nd in node.nbrs]))
                queue.extend(node.children)            
                visited.append(node.name)
