import numpy as np

class BNNode(object):
    """
    """
    def __init__(self, name=None):
        
        self.name = name
        self.parents  = []
        self.children = []
        self.values   = []
        self.localDistribution = None


class MNNode(object):
    """
    """
    def __init__(self, name=None):
        
        self.name = name
        self.nbrs  = []
        self.values   = []
        self.localDistribution = None
