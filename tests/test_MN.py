import unittest
from pgm.helpers.common import Node
from pgm.helpers.search import dfs
from pgm.representation.LinkedListMN import Graph


class TestGraphMethods(unittest.TestCase):

    def test_node_addition(self):
        rootNode = Node('rootNode')
        graph = Graph(rootNode)
        graph.add_node('node1', ['rootNode'])
        graph.add_node('node2', ['rootNode'])
        self.assertEqual(len(rootNode.nbrs), 2)


    def test_search_node(self):
        rootNode = Node('rootNode')
        graph = Graph(rootNode)
        graph.add_node('node1', ['rootNode'])
        graph.add_node('node2', ['rootNode'])

        node1 = dfs(rootNode, 'node1', type = 'MN').searchNode
        node2 = dfs(rootNode, 'node2', type = 'MN').searchNode
        self.assertEqual(node1.name, 'node1')
        self.assertEqual(node2.name, 'node2')


    def test_edge_addition(self):
        rootNode = Node('rootNode')
        graph = Graph(rootNode)
        graph.add_node('node1', ['rootNode'])
        graph.add_node('node2', ['rootNode'])
        graph.add_edge('node2', 'node1')
        node1 = dfs(rootNode, 'node1', type = 'MN').searchNode
        self.assertEqual(node1.name, 'node1')
        self.assertEqual(len(node1.nbrs), 2)

if __name__ == '__main__':
    unittest.main()
