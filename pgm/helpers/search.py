import numpy as np


class dfs(object):
    """
    """
    def __init__(self, root, nodeName=None):
        self.root = root
        self.nodeName = nodeName
        self.visitedNode = []
        self.searchNode = self.search(nodeName)

    def search(self, root):
        """
        """
        self.visitedNode.append(root.name)
        if len(root.children) == 0:
            return -1
        elif root.name == self.nodeName:
            return root
        else:
            for childNode in root.children:
                if not childNode.name in self.visitedNode:
                    node = self.search(childNode)
                    if node.name == root.name:
                        return node



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
