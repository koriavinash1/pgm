import unittest
from pgm.helpers.common import Node
from pgm.helpers.search import dfs
from pgm.representation.LinkedListBN import Graph


class TestGraphMethods(unittest.TestCase):

    def test_node_addition(self):
        rootNode = Node('rootNode')
        graph = Graph(rootNode)
        graph.add_node('node1', 'rootNode')
        graph.add_node('node2', 'rootNode')
        self.assertEqual(len(rootNode.children), 2)


    def test_search_node(self):
        rootNode = Node('rootNode')
        graph = Graph(rootNode)
        graph.add_node('node1', 'rootNode')
        graph.add_node('node2', 'rootNode')

        node1 = dfs(rootNode, 'node1').searchNode
        node2 = dfs(rootNode, 'node2').searchNode
        self.assertEqual(node1.name, 'node1')
        self.assertEqual(node2.name, 'node2')


    def test_edge_addition(self):
        rootNode = Node('rootNode')
        graph = Graph(rootNode)
        graph.add_node('node1', 'rootNode')
        graph.add_node('node2', 'rootNode')
        graph.add_edge('node2', 'node1')
        node2 = dfs(rootNode, 'node2').searchNode
        self.assertEqual(node2.name, 'node2')
        self.assertEqual(len(node2.parents), 2)

if __name__ == '__main__':
    unittest.main()
