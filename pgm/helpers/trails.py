import numpy as np
from .common import Node
from .search import dfs


class findTrails(object):
    """
    """
    def __init__(self, rootNode, nodeA, nodeB):
        """
        """
        nodeA = dfs(rootNode, nodeA).searchNode
        nodeB = dfs(rootNode, nodeB).searchNode
        self.trails = []
        current = []
        current.append(nodeA)
        self.findTrial(nodeA, nodeB, current)


    def findTrial(self, nodeA, nodeB, current):
        """
        """
        current = current.copy()
        if nodeA == None:
            return False

        if nodeA.name == nodeB.name:
            self.trails.append(current)
            return True

        for child in nodeA.children:
            current.append(child)
            self.findTrial(child, nodeB, current)
            current.pop()

    
    def print(self):
        """
        """
        trails = []
        for trail in self.trails:
            ctrail = []
            for node in trail:
                ctrail.append(node.name)
            trails.append(ctrail)
        print(trails)
