import numpy as np

class Node(object):
    r"""
    Commom Node defn for both BN and MN

    Includes ndr attribute for MN
    and includes parents and children for BN
    values for {set of values that node 
    distribution takes}
    """
    def __init__(self, name=None):
            
        self.name = name
        self.parents  = []
        self.children = []
        self.nbrs = []
        self.values   = []
        self.localDistribution = None


