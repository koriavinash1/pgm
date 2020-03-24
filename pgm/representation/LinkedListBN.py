import numpy as np
from ..helpers.common import BNNode as Node
from ..helpers.search import dfs

class Graph(object):
    """
        Adjancency list and Adjancency matrix 
        representation of the graph based on the input 
    """
    def __init__(self, root):
        """
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
        """
            adds node in the graph 
            node: can be ['int', 'str']
            parentNode: can be ['int', 'str']
        """
        parentNode = dfs(self.rootNode, parentNode).searchNode
        if parentNode == -1:
            raise ValueError("parentNode not found")

        node = Node(node)
        node.parents.append(parentNode)
        parentNode.children.append(node)


    def add_edge(self, node1, node2):
        """
            adds edge netween node1 and node2
            node1 -> node2
            node1: can be ['int', 'str']
            node2: can be ['int', 'str']
        """
        node1 = dfs(self.rootNode, node1).searchNode
        node2 = dfs(self.rootNode, node2).searchNode
        if (node1 == -1) or (node2 == -1):
            raise ValueError("Node1 or Node2 not found")
        node1.children.append(node2)
        node2.parents.append(node1)

    def delete_edge(self, node1, node2):
        """
            removes edge between node1 and node2
            deletes node1->node2 edge

            node1: can be ['int', 'str']
            node2: can be ['int', 'str']
        """
        node1 = dfs(self.rootNode, node1).searchNode
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
        """
            removes all the edges and node from the graph

            node: can be ['int', 'str']
        """
        node = dfs(self.rootNode, node).searchNode

        if not (node == -1):
            pass
        
        for  i, chnode in enumerate(node.children):
            for j, pnode in enumerate(chnode.parents):
                if pnode.name == node.name:
                    chnode.parents.pop(j)
                    break
            node.children.pop(i)

        del node
        pass


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


