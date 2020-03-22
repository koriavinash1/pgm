import numpy as np

class findTrails(object):
    """
    """
    def __init__(self, nodeA, nodeB):
        """
        """
        self.trails = []
        self.findTrial(nodeA, nodeB, [nodeA])
        return self.trails


    def findTrial(self, nodeA, nodeB, current):
        """
        """
        if nodeA == None:
            return False

        if nodeA.name == nodeB.name:
            self.trails.append(current)
            return True

        for child in nodeA.children:
            self.findTrial(child, nodeB, current.append(child))
        pass


