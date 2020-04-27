import numpy as np


class loopyBPSegmentation(object):
    """
    """
    def __init__(self, edge_potential, node_potential, input_image, noisy_image):
        """
        """
        self.edge_potential = edge_potential
        self.node_potential = node_potential

        # noise free
        self.input_image    = input_image
        self.noisy_image    = noisy_image

    def mu(self, ii, jj, visited, mu):
        """
        """
        assert self.noisy_image.shape == self.input_image.shape == visited.shape
        if (ii  >= self.noisy_image.shape[0]) or\
            (jj >= self.noisy_image.shape[1]) or \
            (ii < 0) or (jj  < 0) or visited[ii,jj]:
            return mu, visited
        
        # get p based on conditional
        mu[ii, jj] = self.edge_potential[self.noisy_image[ii+1, jj], self.noisy_image[ii, jj]] *\
                     self.edge_potential[self.noisy_image[ii, jj], self.noisy_image[ii, jj+1]] *\
                     self.node_potential[self.noisy_image[ii, jj], self.input_image[ii, jj]]
        
        visited[ii, jj] = 1.0

        mu, visited = self.mu(ii-1, jj, visited, mu)
        mu, visited = self.mu(ii, jj-1, visited, mu)
        mu, visited = self.mu(ii+1, jj, visited, mu)
        mu, visited = self.mu(ii, jj+1, visited, mu)
        return mu, visited


    def message(self, ii, jj, message_matrix, type='f'):
        r"""
        m_{ii->jj}
        x : {0, 1} random matrix
        ii: tuple(x,y)
        jj: tuple(x,y) 
        """
        if (jj[0]  >= self.noisy_image.shape[0]) or (ii[1] >= self.noisy_image.shape[1]) or \
           (ii[0]  >= self.noisy_image.shape[0]) or (jj[1] >= self.noisy_image.shape[1]) or \
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
            message_matrix[ii[0], ii[1], idx, :] = message*self.message(nbr, ii, message_matrix)

        if type == 'f':
            message0 = self.node_potential[self.noisy_image[jj[0], jj[1]], self.input_image[jj[0], jj[1]]]*\
                    (message[0]*self.edge_potential[0, 0] + message[1]*self.edge_potential[1, 0])
            message1 = self.node_potential[self.noisy_image[jj[0], jj[1]], self.input_image[jj[0], jj[1]]]*\
                    (message[0]*self.edge_potential[0, 1] + message[1]*self.edge_potential[1, 1])
            message_matrix[ii[0], ii[1], idx, :]  = np.array([message0, message1])
            print (message_matrix[ii[0], ii[1], idx, :])

        return message_matrix[ii[0], ii[1], idx, :]

    def LBP(self):
        r"""

        x : {0,1} random matrix
        """
        message_to = -np.ones(self.noisy_image.shape + (4, 2,)) # message to i,j
        message_from = -np.ones(self.noisy_image.shape + (4, 2,)) # message from i,j
        op = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for i in range(self.noisy_image.shape[0]):
            for j in range(self.noisy_image.shape[1]):
                count = 0
                for ii, jj in op:
                    message_to[i, j, count, :] = self.message((i+ii, j+jj), (i, j), message_to, type = 'b')
                    # message_from[i, j, count, :] = self.message((i, j), (i+ii, j+jj), message_from)
                    count += 1

        return message_to, message_from


    def segment(self):
        r"""
        """
        while True:
            message_to, message_from = self.LBP()
            message = np.prod(message_to, axis=2)
            self.noisy_image = np.argmax(message, axis=-1)
            yield self.noisy_image
                


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    theta = 0.2; phi=0.5

    edge_potential = np.array([[1+theta, 1-theta],
                                [1-theta, 1+theta]])
    node_potential = np.array([[1+phi, 1-phi],
                                [1-phi, 1+phi]]) 

    input_image = np.zeros((12,12)).astype('int')
    input_image[5:9, 5:9] = 1

    noisy_image = np.random.randint(0,2, size=(12,12))
    noisy_image = input_image*noisy_image.astype('int')
    
    lbpsegmentor = loopyBPSegmentation(edge_potential, 
                    node_potential, 
                    input_image, 
                    noisy_image)

    epochs = 10
    plt.ion()
    x = noisy_image
    for i in range(epochs):
        plt.clf()
        plt.subplot(1, 2, 1)
        plt.imshow(input_image)
        plt.subplot(1, 2, 2)
        plt.imshow(x)
        plt.pause(0.5)
        x = next(lbpsegmentor.segment())