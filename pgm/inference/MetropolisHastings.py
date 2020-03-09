import numpy as np
import math
import pandas as pd
import matplotlib.pyplot as plt 


class MH(object):
    def __init__(self, function, nMontecarlo, proposalDistribution ='gaussion', threshold=None):
        self.fucntion = function
        self.nMontecarlo = nMontecarlo
        self.proposalDistribution = proposalDistribution
        self.x = np.random.randn()
        self.threshold = threshold


    def check_point(self, x_next):
        minval = min(1, self.function(x_next)/self.function(self.x))
        if type(self.threshold) == str:
            self.threshold = np.random.uniform(0,1)

        if minval > self.threshold:
            self.x = x_next

    def sampler(self):
        while True:
            for i in range(self.nMontecarlo):
                x_next = np.random.normal(self.x, 2)
                self.check_point(x_next)
            yield self.x


