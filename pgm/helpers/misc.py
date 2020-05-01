import numpy as np
from .common import Node
from .search import dfs
from ..representation.LinkedListBN import Graph as BNGraph
from ..representation.LinkedListMN import Graph as MNGraph


class GenerateRandomGraph(object):
	r""" Generates graph skeleton randomly

	"""
	def __init__(self, N, type='BN', skeleton_only=True):
		r"""

		N : number of nodes
		type : ['BN' or 'MN']; Bayesian Network or Markov Network
		skeleton_only: bool, if no distribution is not generated
		"""
		self.N = N
		self.type = type
		self.skeleton_only = skeleton_only
		self.rootNode = 'rootNode'
		self.current_nodes = [self.rootNode]

		if self.type == 'BN': self.Graph = BNGraph(self.rootNode)
		elif self.type == 'MN': self.Graph = MNGraph(self.rootNode)
		else : raise ValueError("Invalid type argument. Allowed values ['BN', 'MN']")

		self.create_graph()


	def create_graph(self):
		r""" Creates random bayesian network
		"""	

		for nidx in range(self.N-1):
			nnodes = np.random.randint(1, len(self.current_nodes)+1)
			node_idxs  = np.random.randint(0, len(self.current_nodes), 
										nnodes)
			nodes  = np.array(self.current_nodes)[node_idxs]

			node_name = 'node'+str(nidx + 1)
			self.Graph.add_node(node_name, 
								nodes)
			self.current_nodes.append(node_name)