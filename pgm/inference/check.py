
 
import numpy as np
import pandas as pd
from scipy.stats import gamma
import matplotlib.pyplot as plt
import cv2

class Loopy():

	def __init__(self, grid, iterations):
		self.grid = grid
		self.size = self.grid.shape[0]
		self.iterations = iterations
		self.compatibility_inter = np.array([[1.5, 0.5], [0.5, 1.5]])
		self.compatibility_outer = np.array([[1.9, 0.1], [0.1, 1.9]])

	def get_neighbours(self, idx):

		neighbours = []
		if idx+self.size < self.size**2:
			neighbours.append(idx+self.size)
		if idx-self.size > 0:
			neighbours.append(idx-self.size)
		try:
			if np.unravel_index(idx-1, (self.size,self.size))[0] ==  np.unravel_index(idx, (self.size,self.size))[0]:
				neighbours.append(idx-1)
		except:
			pass
		try:
			if np.unravel_index(idx+1, (self.size,self.size))[0] ==  np.unravel_index(idx, (self.size,self.size))[0]:
				neighbours.append(idx+1)
		except:
			pass

		return(neighbours)

	def message_dict(self, iterations):

		factor_messages = np.ones((self.size**2, self.size**2, 2))
		clique_messages = np.ones((self.size**2, self.size**2, 2))
		beta = np.ones((self.size, self.size, 2))

		for i in range(iterations):
			for j in range(self.size**2):
				neighbours = self.get_neighbours(j)
				for n in neighbours:
					factor_messages[j,n,:] = self.compatibility_outer[:, self.grid[np.unravel_index(j, (self.size, self.size))]]
					adj_neighbours = np.setdiff1d(neighbours,n)
					for adj in adj_neighbours:
						factor_messages[j,n,:] *= clique_messages[adj,j,:]
					clique_messages[n,j,:] *= self.compatibility_inter.dot(factor_messages[n,j,:])
			factor_norm = np.sum(factor_messages, axis=2)
			factor_messages[:,:,0] /= factor_norm
			factor_messages[:,:,1] /= factor_norm
			clique_norm = np.sum(clique_messages, axis=2)
			clique_messages[:,:,0] /= clique_norm
			clique_messages[:,:,1] /= clique_norm

		for j in range(self.size**2):
			neighbours = self.get_neighbours(j)
			for n in neighbours:
				beta[np.unravel_index(j, (self.size, self.size))] *= factor_messages[j,n]

		plt.imshow(np.argmax(beta, axis = 2))
		plt.show()

	# def message_dict(self, iterations):

	# 	factor_messages = np.ones((self.size**2, self.size**2, 2))
	# 	clique_messages = np.ones((self.size**2, self.size**2, 2))
	# 	beta = np.ones((self.size, self.size, 2))

	# 	for i in range(iterations):
	# 		for j in range(self.size**2):
	# 			neighbours = self.get_neighbours(j)
	# 			for n in neighbours:
	# 				factor_messages[j,n,:] = self.compatibility_outer[:, self.grid[np.unravel_index(j, (self.size, self.size))]]
	# 				adj_neighbours = np.setdiff1d(neighbours,n)
	# 				for adj in adj_neighbours:
	# 					factor_messages[j,n,:] *= clique_messages[adj,j,:]
	# 				clique_messages[n,j,:] *= self.compatibility_inter.dot(factor_messages[n,j,:])
	# 		factor_norm = np.sum(factor_messages, axis=2)
	# 		factor_messages[:,:,0] /= factor_norm
	# 		factor_messages[:,:,1] /= factor_norm
	# 		clique_norm = np.sum(clique_messages, axis=2)
	# 		clique_messages[:,:,0] /= clique_norm
	# 		clique_messages[:,:,1] /= clique_norm
	# 		# print(factor_messages, clique_messages)

	# 	for j in range(self.size**2):
	# 		neighbours = self.get_neighbours(j)
	# 		for n in neighbours:
	# 			beta[np.unravel_index(j, (self.size, self.size))] *= factor_messages[j,n]
	# 		# print(self.compatibility_outer[:, self.grid[np.unravel_index(j, (self.size, self.size))]])
	# 		# beta[np.unravel_index(j, (self.size, self.size))] *= self.compatibility_outer[:, self.grid[np.unravel_index(j, (self.size, self.size))]]
	# 	plt.imshow(np.argmax(beta, axis = 2))
	# 	plt.show()


if __name__ == '__main__':

	size = 60
	flip_prob = 0.2
	grid = np.zeros((size, size), dtype='int64')
	for j in range(size**2):
		idx = np.unravel_index(j, (size, size))
		if ((idx[0]-50)**2+(idx[1]-50)**2)**0.5 <= 25:
			grid[idx] = 1
		thresh = np.random.random_sample()
		if thresh < flip_prob:
			grid[idx] = 1-grid[idx]

	plt.imshow(grid)
	plt.show()
	L = Loopy(grid, 10)
	L.message_dict(10)