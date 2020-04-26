import numpy as np
from ..helpers.common import Node
from ..helpers.search import dfs

class Graph(object):
    r""" Adjancency list and Adjancency matrix 
    representation of the graph based on the input 
    """
    def __init__(self, root):
        r"""

        root: node<object> or str
            if str it'll generate node and the following graph
        """
        self.nodesPresent = []

        if isinstance(root, Node):
            self.rootNode = root
        elif isinstance(root, str) or isinstance(root, int):
            self.rootNode = Node()
            self.rootNode.name = root
        else:
            raise ValueError("Invalid type for root argument")


    def add_node(self, node, parentNode):
        r""" adds node in the graph 
        
        node: can be ['int', 'str'] or Node object
        parentNode: can be ['int', 'str'] or Node object
        """

        if not isinstance(parentNode, Node):
            parentNode = dfs(self.rootNode, parentNode).searchNode

        if parentNode == -1:
            raise ValueError("parentNode not found")

        if not isinstance(node, Node):
            node = Node(node)
        node.parents.append(parentNode)
        parentNode.children.append(node)


    def add_edge(self, node1, node2):
        r"""adds edge netween node1 and node2
            node1 -> node2
            
        node1: can be ['int', 'str'] or Node object
        node2: can be ['int', 'str'] or Node object
        """
        if not isinstance(node1, Node):
            node1 = dfs(self.rootNode, node1).searchNode

        if not isinstance(node2, Node):
            node2 = dfs(self.rootNode, node2).searchNode
        
        if (node1 == -1) or (node2 == -1):
            raise ValueError("Node1 or Node2 not found")
        
        node1.children.append(node2)
        node2.parents.append(node1)


    def delete_edge(self, node1, node2):
        r"""removes edge between node1 and node2
            deletes directed edge from node1->node2

        node1: can be ['int', 'str'] or Node object
        node2: can be ['int', 'str'] or Node object
        """

        if not isinstance(node1, Node):
            node1 = dfs(self.rootNode, node1).searchNode

        if not isinstance(node2, Node):
            node2 = dfs(self.rootNode, node2).searchNode

        if (node1 == -1) or (node2 == -1):
            raise ValueError("Node1 or Node2 not found")
        
        for i, child in enumerate(node1.children):
            if child.name == node2.name:
                node1.children.pop(i)
                break

        for i, parent in enumerate(node2.parents):
            if parent.name == node1.name:
                node2.parents.pop(i)
                break
        return


    def delete_node(self, node):
        r""" removes all the edges and node from the graph

        node: can be ['int', 'str'] or Node object
        """

        if not isinstance(node, Node):
            node = dfs(self.rootNode, node).searchNode

        if (node == -1):
            raise ValueError("Node doesn't exist")
        
        for  i, chnode in enumerate(node.children):
            for j, pnode in enumerate(chnode.parents):
                if pnode.name == node.name:
                    chnode.parents.pop(j)
                    break
            node.children.pop(i)

        del node
        pass


    def get_node(self, node):
        r""" search and returns the node

        node: can be ['int', 'str']
        """
        node = dfs(self.rootNode, node).searchNode

        if (node == -1):
            raise ValueError("Node doesn't exist")

        return node 

    def calculate_conditional(self, nodes, values):
        r""" calculates conditional distribution fixing the
        values of given nodes

        nodes: can be list of ['int', 'str' or Node object]
        values: [node_value in same order]
        """

        raise NotImplementedError()


    def calculate_marginals(self, nodes):
        r""" removes the node and restimates marginals

        nodes: can be list of ['int', 'str' or Node object]
        """

        raise NotImplementedError()
        

    def print(self, node):
        if node == None:
            return

        queue = [node]
        visited = []

        for node in queue:
            if not node.name in visited:
                print("node: {}, children: {}, parents: {}".format(node.name, 
                                            [nd.name for nd in node.children], 
                                            [nd.name for nd in node.parents]))
                queue.extend(node.children)            
                visited.append(node.name)