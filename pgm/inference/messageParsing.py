import numpy as np
from ..helpers.common import Node
from ..helpers.search import dfs

class MessageParsing(object):
    r""" message parsing algorithm

    KF Book: chapter 7
    """

    def __init__(self, rootNode, type='BN'):
    	r"""

    	rootNode: Node attribute
    	type : 'BN' or 'MN'
    	"""
    	self.type = type
    	if isinstance(root, Node):
            self.rootNode = root

    def parse_message(self, node1, node2):
    	r""" Caclulates the message from node1 -> node2
		message_{node1->node2} = 
			\sum_{node1} \phi(node1)\phi(node1, node2)
				\prod_{pa \in parents_{node1}} message_{pa->node1}

		node1: ['int' or 'str'] or <Node> object
		node2: ['int' or 'str'] or <Node> object
    	"""

		if not isinstance(node1, Node):
			node1 = dfs(self.rootNode, node1, self.type).searchNode

        if not isinstance(node2, Node):
			node2 = dfs(self.rootNode, node2, self.type).searchNode

		if self.type=='BN':
			assert node2 in node1.children, "No direct link between node1 and node2"
		else:
			assert node2 in node1.nbrs, "No direct link between node1 and node2"

		