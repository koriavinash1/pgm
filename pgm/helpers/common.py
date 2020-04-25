import numpy as np

class Node(object):
    r""" Commom Node defn for both BN and MN

    Includes ndr attribute for MN
    and includes parents and children for BN
    values for {set of values that node 
    distribution takes}
    """
    def __init__(self, name=None):
            
        self.name = name
        
        # present only for BN
        self.parents  = []
        self.children = []

        # present only for MN
        self.nbrs = []
        self.values   = []
        self.localDistribution = None


    def set_distribution(self, probabilities = None, type='BN'):
        r""" sets a local probabilities distribution
        
        type: ['BN', 'MN']

        probabilities: json, None
            if None: Interactive mode will be triggered
            json: {((pnode_names), (pnode_values)): {nvalue: probability}}
        """
        parent_nvalues = [len(node.values) for node in self.parents]

        if not probabilities:
            nprobabilities = len(probabilities.keys())*len(probabilities.values()[0].keys())
            assert nprobabilities == np.prod(parent_nvalues)*len(self.values),\
                         "Incomplete distribution Provided"
            self.localDistribution = probabilities

        else:
            parent_names = [node.name for node in self.parents]
            parent_values = []
            self.localDistribution = {} 

            def _value_tuple(i, j, tuple):
                if i == len(self.parents) -1:
                    return tuple

                pnode = self.parents[i]
                tuple = tuple + (pnode.values[j], )
                for jj in range(j, len(pnode.values)):
                    tuple = _value_tuple(i+1, j+jj, tuple)
                    parent_values.append(tuple)

                return tuple

            for pnodes in parent_names:
                for pvalues in parent_values:
                    proability = raw_input("Parent Names: {} = Values: {}".format(pnodes, pvalues))
                    self.localDistribution[(pnodes, pvalues)] = {self.values: proability} 

        return pass


    def calculate_conditional(self):
        pass


