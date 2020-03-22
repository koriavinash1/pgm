import numpy as np
from .common import Node

class dfs(object):
    """
    """
    def __init__(self, root, nodeName=None):
        self.root = root
        self.nodeName = nodeName
        self.visitedNode = []
        self.searchNode = self.search(self.root)

     
    def search(self, root):
        """
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
    """
    def __init__(self, root, nodeName):
        """
        """
        self.root = root
        self.nodeName = nodeName
        self.visitedNode = []
        self.searchNode = self.search(nodeName)

    def search(self, root):
        """
        """
        queue = [root]

        for node in queue:
            if node.name == self.searchNode:
                return node

            if not node.name in self.visitedNode:
                queue.extend(node.children)
                self.visitedNode.append(node.name)
