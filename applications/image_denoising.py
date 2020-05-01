import numpy as np

class loopyBPDenoising(object):
    r"""
    """
    def __init__(self, edge_potential, node_potential, input_image, noisy_image, normed=True):
        r"""
        """
        self.edge_potential = edge_potential
        self.node_potential = node_potential

        # noise free
        self.input_image    = input_image
        self.noisy_image    = noisy_image
        self.nbeliefs  = 2

        self.normed = normed

    def mu(self, ii, jj, visited, mu):
        r"""
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

    def _conj(self, i, j, c):
        r""" estimates the conjugate coordinates

        """
        nbr_op   = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        if c == 0: 
            return i, j+1, 1
        elif c == 1: 
            return i, j-1, 0
        elif c == 2: 
            return i-1, j, 3
        else: 
            return i+1, j, 2

    def message(self, message_matrix):
        r"""
        m_{ii->jj}
        x : {0, 1} random matrix
        ii: tuple(x,y)
        jj: tuple(x,y) 

        mi→a(xi) = \prod_c∈Neighbour(i)\a mc→i(xi) 
        ma→i(xi) = \sum_Xa\xi fa(Xa) \prod_j∈Neighbour(a)\i mj→a(xj ) (11)
        """

        nbr_op   = [(0, 1), (0, -1), (-1, 0), (1, 0)]
        for i in range(self.noisy_image.shape[0]):
            for j in range(self.noisy_image.shape[1]):
                nbrs = []
                for idx, (ii, jj) in enumerate(nbr_op):
                    try: 
                        _=self.noisy_image[i+ii,j+jj]
                        nbrs.append(idx)
                    except: pass

                for c, nb in enumerate(nbrs):
                    message_matrix[i, j, nb, 0, :] = self.node_potential[:, self.noisy_image[i, j]]
                    for nbc in np.delete(nbrs, c):
                        message_matrix[i, j, nb, 0, :] *= message_matrix[i, j, nbc, 1, :]
                    ic, jc, cc = self._conj(i, j, nb)
                    message_matrix[i, j, nb, 1, :] *= self.edge_potential.dot(message_matrix[ic, jc, cc, 0, :])
                
        Z = np.sum(message_matrix, axis=-1)
        for i in range(self.nbeliefs):
            message_matrix[..., i] /= Z

        return message_matrix


    def LBP(self):
        r"""

        x : {0,1} random matrix
        """
        message_matrix = np.ones(self.noisy_image.shape + (4, 2, self.nbeliefs,)) # message to i,j
        while  True:
            message_matrix = self.message(message_matrix)
            message = np.prod(message_matrix[:,:,:,1,:], axis=2)
            self.noisy_image = np.argmax(message, axis=-1)
            yield self.noisy_image
                


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    theta = 0.5; phi=0.5

    edge_potential = np.array([[1+theta, 1-theta],
                                [1-theta, 1+theta]])
    node_potential = np.array([[1+phi, 1-phi],
                                [1-phi, 1+phi]]) 


    size = 100
    flip_prob = 0.2
    radius = 25
    center = (50, 50)
    input_image = np.zeros((size, size), dtype='uint8')
    noise = np.random.uniform(0, 1, (size, size))

    for ix in range(size):
        for iy in range(size):
            if ((ix-center[0])**2+(iy-center[1])**2)**0.5 <= radius:
                input_image[ix, iy] = 1

    noisy_image = input_image.copy()
    noisy_image[noise<flip_prob] = 1-noisy_image[noise<flip_prob]

    count = []
    for _ in range(25):
        lbpsegmentor = loopyBPDenoising(edge_potential, 
                        node_potential, 
                        input_image, 
                        noisy_image)

        epochs = 1
        x = noisy_image
        for i in range(epochs):
            x = next(lbpsegmentor.LBP())

        count.append(np.sum(x == input_image))

    plt.subplot(1, 3, 1)
    plt.imshow(input_image)
    plt.xticks([],'')
    plt.yticks([],'')
    plt.xlabel("Noise free image")
    plt.subplot(1, 3, 2)
    plt.imshow(noisy_image)
    plt.xticks([],'')
    plt.yticks([],'')
    plt.xlabel("Noisy image")
    plt.subplot(1, 3, 3)
    plt.imshow(x)
    plt.xticks([],'')
    plt.yticks([],'')
    plt.xlabel("Denoised image")
    plt.title(str(np.mean(count)))
    plt.show()