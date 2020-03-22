import numpy as np
from .common import Node

class dfs(object):
    """
        This class implements depth first search algorithm
        is used to search for specific node given rootnode
    """
    def __init__(self, root, nodeName=None):
        """
            root: root node of the graph
                  graph in linkedlist format
            nodeName: str: node to search 
                  in the graph
        """
        self.root = root
        self.nodeName = nodeName
        self.visitedNode = []
        self.searchNode = self.search(self.root)

     
    def search(self, root):
        """
            reccursive function for searching node
        """
        self.visitedNode.append(root.name)

        if root.name == self.nodeName:
            return root

        elif len(root.children) == 0:
            return -1

        else:
            for childNode in root.children:
                if not childNode.name in self.visitedNode:
                    node = self.search(childNode)

                    if isinstance(node, Node):
                        if node.name == self.nodeName:
                            return node      
            return -1 



class bfs(object):
    """
        This class implements breath first search algorithm
        is used to search for specific node given rootnode
    """
    def __init__(self, root, nodeName):
        """
            root: root node of the graph
                  graph in linkedlist format
            nodeName: str: node to search 
                  in the graph
        """
        self.root = root
        self.nodeName = nodeName
        self.visitedNode = []
        self.searchNode = self.search(nodeName)

    def search(self, root):
        """
           queue implemetation for bfs
        """
        queue = [root]

        for node in queue:
            if node.name == self.searchNode:
                return node

            if not node.name in self.visitedNode:
                queue.extend(node.children)
                self.visitedNode.append(node.name)
