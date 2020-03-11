import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt 


def proposalDistribution(sigma=2):
    """
        Describes example proposal distribution
        considers gaussion distribution with fixed sigma

        as the mean keeps changing it's made an inner function argument
    """
    def QDistribution(param = 0):
        return lambda x: (1/((2*np.pi)**0.5 * sigma))*np.exp((x-param)**2/ sigma**2)
    return QDistribution


class MH(object):
    """
        This class implements the MH algorithm for any given 
        distribution and proposal fucntions

        It checks the conditions for proposal functions
        which confirms stationarity

        Estimates Acceptance probability for new proposals
        if accepted saves the value in x_seq list
    """

    def __init__(self, function, burninT, proposalDistribution = proposalDistribution(), proposalSampler = None):
        """
            function: <lambda or any function> complex distribution to 
                        sample points
            burinT  : <int> number of burnin iterations 
            proposalDistribution: <lambda or any function> simple 
                        distribution

        """
        self.function = function
        self.burninT = burninT
        self.nonSymmetricP = True
        self.proposalDistribution = proposalDistribution
        self.proposalSampler = proposalSampler

        self.check_proposalDistribution()
        self.x = np.random.rand()
        self.x_seq = []

    
    def check_proposalDistribution(self):
        """
            checks for stationarity and symmetiricity
            
        """
        # Symmetry check:
        Q_x = self.proposalDistribution(param = 0)(0.5)
        Q_xn = self.proposalDistribution(param = 0.5)(0)
        if np.abs(Q_x - Q_xn) < 1e-3:
            self.nonSymmetricP = False

    def check_point(self, x_next):
        """
            computes Acceptance probability 
            A(X'|X) = min(1, P(X')Q(X|X')/(P(X)Q(X'|X)

            accept next point if it's greater than the 
            threshold

            x_next: can be scalar or numpy array
                    based on dimensionality of probability
                    distribution

        """
        if self.nonSymmetricP:
            Q_x = self.proposalDistribution(param = self.x)(x_next)
            Q_xnext = self.proposalDistribution(param = x_next)(self.x)

            A_xn = min(1, (self.function(x_next)*Q_x)/(self.function(self.x)*Q_xnext))
        else:
            A_xn = min(1, self.function(x_next)/self.function(self.x))
        
        # print(A_xn, self.function(x_next), self.function(self.x), x_next, self.x)
        self.threshold = np.random.uniform(0,1)
        if A_xn > self.threshold:
            self.x = x_next

    def sampler(self):
        """
            Sampler returns a value after burninT
            
            returns: iterator
        """
        while True:
            for i in range(self.burninT):
                x_next = self.proposalSampler(self.x)
                self.check_point(x_next)
            self.x_seq.append(self.x)
            yield self.x


