import numpy as np
from .common import Node
from .search import dfs


class findTrails(object):
    """
       This class imlpemets a method to find trails
       between nodeA and nodeB
    """
    def __init__(self, rootNode, nodeA, nodeB, type='BN'):
        """
            rootNode: rootnode of a graph
            nodeA: str:
            nodeB: str:

            trails from nodeA to nodeB (nodeA ~> nodeB)
        """
        self.type = type

        nodeA = dfs(rootNode, nodeA, type = self.type).searchNode
        nodeB = dfs(rootNode, nodeB, type = self.type).searchNode
        self.trails = []
        current = []
        current.append(nodeA)
        self.findTrial(nodeA, nodeB, current)


    def findTrial(self, nodeA, nodeB, current):
        """
            reccursive implementation for estimating all trails
        """
        current = current.copy()
        if nodeA == None:
            return False

        if nodeA.name == nodeB.name:
            self.trails.append(current)
            return True
        
        if self.type == 'BN':
            for child in nodeA.children:
                current.append(child)
                self.findTrial(child, nodeB, current)
                current.pop()
        elif self.type == 'MN':
            for child in nodeA.nbrs:
                current.append(child)
                self.findTrial(child, nodeB, current)
                current.pop()
        else:
            raise ValueError("Unkown type variable")
    
    def print(self):
        """
            prints all trails in str format
        """
        trails = []
        for trail in self.trails:
            ctrail = []
            for node in trail:
                ctrail.append(node.name)
            trails.append(ctrail)
        print(trails)
