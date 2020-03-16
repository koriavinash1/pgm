import numpy as np


class GibbsSampler(object):
    """
    """
    def __init__(self, local_distribution, burninT, Xnodes, Ynodes):
        """
        """
        self.local_distribution = local_distribution
        self.burninT = burninT
        self.Xnodes = Xnodes
        self.Ynodes = Ynodes
        # sample x
        self.x = np.round(np.random.uniform(0, 1, \
                        (self.Xnodes, self.Ynodes)))
        self.count_seq = []
        self.x_seq = []
        
    def getConditional(self, x, i, j):
        """
        """
        nbr_pairs = []
        op = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for ii, jj in op:
            try:
                nbr_pairs.append((x[i,j], x[i+ii, j+jj]))
            except:
                pass
        nr = np.prod([self.local_distribution[nbr_pair] \
                                for nbr_pair in nbr_pairs])
        dr = nr + np.prod([self.local_distribution[(\
                        abs(1-nbr_pair[0]), nbr_pair[1])] \
                            for nbr_pair in nbr_pairs])
        return nr*1./dr

    def localSampler(self, x_next, ii, jj):
        """
        """
        if (ii  >= x_next.shape[0]) or\
            (jj >= x_next.shape[1]) or \
            (ii < 0) or (jj  < 0) or self.visited[ii,jj]:
            return x_next
        
        self.count_seq.append(self.count(x_next))
        # get p based on conditional
        p = self.getConditional(x_next, ii, jj)
        
        # sample xij

        for _ in range(self.burninT):
            xn = x_next[ii, jj] if p > np.random.uniform(0,1) else 1 - x_next[ii, jj]
        
        x_next[ii, jj] = xn
        self.visited[ii, jj] = 1.0

        x_next = self.localSampler(x_next, ii-1, jj)
        x_next = self.localSampler(x_next, ii, jj-1)
        x_next = self.localSampler(x_next, ii+1, jj)
        x_next = self.localSampler(x_next, ii, jj+1)
        return x_next

    def Proposal(self, ii,jj):
        """
        """
        self.visited = np.zeros_like(self.x)
        x_next = np.copy(self.x)
        x_next = self.localSampler(x_next, ii, jj)
        return x_next

    def countUtils(self, x, c, i, j):
        """
        """
        if (i + 1  >= self.x.shape[0]) or\
            (j + 1 >= self.x.shape[1]) or \
            (i < 0) or (j  < 0) or (self.vis[i,j] == 1):
            return c

        self.vis[i,j] = 1
        if x[i+1, j] == 1.:
            c += self.countUtils(x, c+1, i+1, j)
        elif x[i, j+1] == 1.:
            c += self.countUtils(x, c+1, i, j+1)

        return c

    def count(self, x):
        """
        """
        self.vis = np.zeros_like(x)
        return self.countUtils(x, 0, 0, 0) 
    
    def sampler(self):
        """
        """
        while True:
            ii = np.random.randint(0, self.Xnodes)
            jj = np.random.randint(0, self.Ynodes)
            self.x = self.Proposal(ii, jj)
            self.x_seq.append(self.x)
            yield self.x
                


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    local_distribution = {(1,1): 0.0, 
                          (0,0): 1,
                          (1,0): 1,
                          (0,1): 1}
    gs = GibbsSampler(local_distribution, 10, 24, 24)
    
    epochs = 10
    for i in range(epochs):
        x = next(gs.sampler())
        plt.clf()
        plt.imshow(x)
        plt.show()

        plt.clf()
        plt.plot(gs.count_seq)
        plt.xlabel("mixture progression")
        plt.ylabel("count")
        # plt.title("Epoch: {}".format(i))
        plt.show()

