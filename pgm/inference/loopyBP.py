import numpy as np
import sys
sys.setrecursionlimit(10**6)

class loopyBPSegmentation(object):
    """
    """
    def __init__(self, edge_potential, node_potential, input_image, noisy_image, normed=True):
        """
        """
        self.edge_potential = edge_potential
        self.node_potential = node_potential

        # noise free
        self.input_image    = input_image
        self.noisy_image    = noisy_image

        self.normed = normed

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
            return np.ones_like(message_matrix)*0.5

        op = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        idx_tuple = tuple([jj[0]-ii[0], jj[1] - ii[1]]) if type=='f' else tuple([ii[0]-jj[0], ii[1] - jj[1]])
        for i, _op in enumerate(op):
            if idx_tuple == _op:
                idx = i
                break

        if np.sum(message_matrix[ii[0], ii[1], idx, :]) >= 1.0:
            return message_matrix

        nbrs = [(ii[0], ii[1]+1), (ii[0], ii[1]-1), (ii[0]-1, ii[1]), (ii[0]+1, ii[1])]
        nbrs = [nbr for nbr in nbrs if not (nbr == jj)]

        message = np.array([.5, .5])
        message_matrix[ii[0], ii[1], idx, :] = message
        for nbr in nbrs:
            message_matrix[ii[0], ii[1], idx, :] *= self.message(nbr, ii, message_matrix)[ii[0], ii[1], idx, :]
            

        message = message_matrix[ii[0], ii[1], idx, :]
        if type == 'f':
            message0 = self.node_potential[0, self.noisy_image[jj[0], jj[1]]]*\
                    (message[0]*self.edge_potential[0, 0] + message[1]*self.edge_potential[1, 0])
            message1 = self.node_potential[1, self.noisy_image[jj[0], jj[1]]]*\
                    (message[0]*self.edge_potential[0, 1] + message[1]*self.edge_potential[1, 1])
            message = np.array([message0, message1])

            if self.normed: message /= np.sum(message)
            message_matrix[ii[0], ii[1], idx, :]  = message

            print (message)
        return message_matrix


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
                    message_to = self.message((i+ii, j+jj), (i, j), message_from, type = 'b')
                    message_from = self.message((i, j), (i+ii, j+jj), message_to)
                    count += 1
                print ("======={}{}=====".format(i,j))

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

    theta = 0.8; phi=0.2

    edge_potential = np.array([[1+theta, 1-theta],
                                [1-theta, 1+theta]])
    node_potential = np.array([[1+phi, 1-phi],
                                [1-phi, 1+phi]]) 

    input_image = np.zeros((25,25)).astype('int')
    input_image[8:17, 8:17] = 1

    noisy_image = np.random.randint(0,2, size=(25,25))
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
        plt.pause(1)
        x = next(lbpsegmentor.segment())