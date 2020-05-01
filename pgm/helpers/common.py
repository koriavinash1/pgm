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
        self.type = 'BN'
        
        # present only for BN
        self.parents  = []
        self.children = []

        # present only for MN
        self.nbrs = []
        self.values   = []
        self.localDistribution = None



    def check(self, string, args=[]):
        r""" Checks for sum of the distribution"""

        temp = {}
        for value in self.values:
            probability = input(string.format(self.name, value, *args))
            temp[value] = float(probability)

        if self.type == 'BN':
            if not np.sum(list(temp.values())) == 1.0 :
                print ("Improper Probability distribution sum != 1. Re-enter the probability values")
                temp = self.check(string, args)
        return temp


    def set_distribution_BN(self, probabilities = None):
        r""" sets a local probabilities distribution
        
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
                self.localDistribution = self.check("CurrentNode: {} | nodeValue: {} | Probability= ")
              
            # parent_names = [node.name for node in self.parents]
            parent_values = []
            parent_names = []

            def _value_tuple(i, j, value_tuple, name_tuple):
                if i >= len(self.parents):
                    return value_tuple, name_tuple

                pnode = self.parents[i]
                for jj in range(j, len(pnode.values)):
                    value_tuple = value_tuple + (pnode.values[jj], )
                    name_tuple  = name_tuple + (pnode.name, )
                    value_tuple, name_tuple = _value_tuple(i+1, j+jj, value_tuple, name_tuple)
                    parent_values.append(value_tuple)
                    parent_names.append(name_tuple)

                    value_tuple = ()
                    name_tuple  = ()
                return value_tuple, name_tuple

            _value_tuple(0, 0, (), ())
            parent_names = list(set(parent_names))
            parent_values = list(set(parent_values))

            for pnodes in parent_names:
                for pvalues in parent_values:
                    self.localDistribution[(pnodes, pvalues)] = self.check("CurrentNode: {} | nodeValue: {} || ParentNodes: {} = ParentValues: {} | Probability = ", [pnodes, pvalues])


    def set_distribution_MN(self, probabilities = None):
        r""" sets a local probabilities distribution
        
        probabilities: json, None
            if None: Interactive mode will be triggered
            json: {((pnode_names), (pnode_values)): {nvalue: probability}}
        """
        factor_nvalues = [len(node.values) for node in self.nbrs]

        if probabilities:
            nprobabilities = len(probabilities.keys())*len(probabilities.values()[0].keys())
            assert nprobabilities == np.prod(factor_nvalues)*len(self.values),\
                         "Incomplete distribution Provided"
            self.localDistribution = probabilities

        else:
            self.localDistribution = {} 

            if len(self.nbrs) == 0:
                self.localDistribution = self.check("CurrentNode: {} | nodeValue: {} | Probability= ")
              
            nbr_names = [node.name for node in self.nbrs]
            nbr_values = []

            def _value_tuple(i, j, tuple):
                if i >= len(self.nbrs):
                    return tuple

                pnode = self.nbrs[i]
                for jj in range(j, len(pnode.values)):
                    tuple = tuple + (pnode.values[jj], )
                    tuple = _value_tuple(i+1, j+jj, tuple)
                    nbr_values.append(tuple)
                    tuple = ()


                return tuple

            _value_tuple(0, 0, ())

            for pnodes in nbr_names:
                for pvalues in nbr_values:
                    self.localDistribution[(pnodes, pvalues)] = self.check("CurrentNode: {} | nodeValue: {} || NbrNodes: {} = NbrValues: {} | Probability = ", [pnodes, pvalues])


    def set_distribution(self, probabilities = None):
        r""" sets a local probabilities distribution
        
        probabilities: json, None
            if None: Interactive mode will be triggered
            json: {((pnode_names), (pnode_values)): {nvalue: probability}}
        """

        if self.type == 'MN':
            self.set_distribution_MN(probabilities)
        else:
            self.set_distribution_BN(probabilities)