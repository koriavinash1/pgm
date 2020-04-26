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


    def check(self, string, type, args=[]):
        r""" Checks for sum of the distribution"""
        
        temp = {}
        for value in self.values:
            probability = input(string.format(self.name, value, *args))
            temp[value] = float(probability)

        if type == 'BN':
            if not np.sum(list(temp.values())) == 1.0 :
                print ("Improper Probability distribution sum != 1. Re-enter the probability values")
                temp = self.check(string, type, args)
        return temp


    def set_distribution(self, probabilities = None, type='BN'):
        r""" sets a local probabilities distribution
        
        type: ['BN', 'MN']

        probabilities: json, None
            if None: Interactive mode will be triggered
            json: {((pnode_names), (pnode_values)): {nvalue: probability}}
        """
        parent_nvalues = [len(node.values) for node in self.parents]

        if probabilities:
            nprobabilities = len(probabilities.keys())*len(probabilities.values()[0].keys())
            assert nprobabilities == np.prod(parent_nvalues)*len(self.values),\
                         "Incomplete distribution Provided"
            self.localDistribution = probabilities

        else:
            self.localDistribution = {} 

            if len(self.parents) == 0:
                self.localDistribution = self.check("CurrentNode: {} | nodeValue: {} | Probability= ", type)
              
            parent_names = [node.name for node in self.parents]
            parent_values = []

            def _value_tuple(i, j, tuple):
                if i >= len(self.parents):
                    return tuple

                pnode = self.parents[i]
                for jj in range(j, len(pnode.values)):
                    tuple = tuple + (pnode.values[jj], )
                    tuple = _value_tuple(i+1, j+jj, tuple)
                    parent_values.append(tuple)
                    tuple = ()


                return tuple

            _value_tuple(0, 0, ())

            print (parent_names, parent_values)
            for pnodes in parent_names:
                for pvalues in parent_values:
                    self.localDistribution[(pnodes, pvalues)] = self.check("CurrentNode: {} | nodeValue: {} || ParentNodes: {} = ParentValues: {} | Probability = ", type, [pnodes, pvalues])
