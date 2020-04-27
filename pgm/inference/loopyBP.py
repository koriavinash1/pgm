import numpy as np


class loopyBPSegmentation(object):
    """
    """
    def __init__(self, edge_potential, node_potential, input_image):
        """
        """
        self.edge_potential = edge_potential
        self.node_potential = node_potential
        self.input_image    = input_image

        
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

    def mu(self, x, y, ii, jj, visited, mu):
        """
        """
        assert x.shape == y.shape == visited.shape
        if (ii  >= x.shape[0]) or\
            (jj >= x.shape[1]) or \
            (ii < 0) or (jj  < 0) or visited[ii,jj]:
            return mu, visited
        
        # get p based on conditional
        mu[ii, jj] = self.edge_potential[x[ii+1, jj], x[ii, jj]] *\
                     self.edge_potential[x[ii, jj], x[ii, jj+1]] *\
                     self.node_potential[x[ii, jj], y[ii, jj]]
        
        visited[ii, jj] = 1.0

        mu, visited = self.mu(x, y, ii-1, jj, visited, mu)
        mu, visited = self.mu(x, y, ii, jj-1, visited, mu)
        mu, visited = self.mu(x, y, ii+1, jj, visited, mu)
        mu, visited = self.mu(x, y, ii, jj+1, visited, mu)
        return mu, visited


    def message(self, x, ii, jj, message_matrix, type='f'):
        r"""

        x : {0, 1} random matrix
        ii: tuple(x,y)
        jj: tuple(x,y) 
        """
        if (jj[0]  >= x.shape[0]) or (ii[1] >= x.shape[1]) or \
           (ii[0]  >= x.shape[0]) or (jj[1] >= x.shape[1]) or \
           (ii[0] < 0) or (jj[0]  < 0) or (ii[1] < 0) or (jj[1]  < 0):
            return 1.0

        op = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        idx_tuple = tuple([jj[0]-ii[0], jj[1] - ii[1]])
        for i, _op in enumerate(op):
            if idx_tuple == _op:
                idx = i
                break

        if message_matrix[ii[0], ii[1], idx, 0] >= 0:
            return message_matrix[ii[0], ii[1], idx, :]

        nbrs = [(ii[0], ii[1]+1), (ii[0], ii[1]-1), (ii[0]-1, ii[1]), (ii[0]+1, ii[1])]
        nbrs = [nbr for nbr in nbrs if not (nbr == jj)]

        message = np.array([1., 1.])
        for nbr in nbrs:
            message = message*self.message(x, nbr, ii)

        if type == 'f':
            message0 = message[0]*self.edge_potential[0, 0] + message[1]*self.edge_potential[1, 0]
            message1 = message[0]*self.edge_potential[0, 1] + message[1]*self.edge_potential[1, 1]
            message  = np.array([message0, message1])

        return message

    def LBP(self, x):
        r"""

        x : {0,1} random matrix
        """
        message_to = -np.ones(x.shape + (4, 2,)) # message to i,j
        message_from = -np.ones(x.shape + (4, 2,)) # message from i,j
        op = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for i in range(x.shape[0]):
            for j in range(x.shape[1]):
                count = 0
                for ii, jj in op:
                    message_to[i, j, count, :] = self.message(x, (i+ii, j+jj), (i, j), message_to, type = 'b')
                    message_from[i, j, count, :] = self.message(x, (i, j), (i+ii, j+jj), message_from)
                    count += 1

        return message_to, message_from


    def segment(self, x):
        r"""
        """
        while True:
            message_to, message_from = self.LBP(x)
            message = np.prod(message_to, axis=2)
            x = np.argmax(message, axis=-1)
            yield x
                


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