import numpy as np

class Node(object):
    """
    """
    def __init__(self, name=None):
        
        self.name = name
        self.parents  = []
        self.children = []
        self.nbrs = []
        self.values   = []
        self.localDistribution = None


