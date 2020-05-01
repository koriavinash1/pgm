pgm\.helpers package
====================

Submodules
----------

pgm\.helpers\.common module
---------------------------

.. automodule:: pgm.helpers.common
    :members:
    :undoc-members:
    :show-inheritance:

pgm\.helpers\.misc module
-------------------------

.. automodule:: pgm.helpers.misc
    :members:
    :undoc-members:
    :show-inheritance:

pgm\.helpers\.search module
---------------------------

.. automodule:: pgm.helpers.search
    :members:
    :undoc-members:
    :show-inheritance:

pgm\.helpers\.trails module
---------------------------

.. automodule:: pgm.helpers.trails
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: pgm.helpers
    :members:
    :undoc-members:
    :show-inheritance:


Search dfs
==========
..code:: python
    from pgm.helpers.search import dfs

    root = rootNode
    searchNode = 'node4'
    node = dfs(root, searchNode).searchNode


GetTrails for BN
======================
..code:: python
    from pgm.helpers.common import Node
    from pgm.representation.LinkedListBN import Graph
    from pgm.helpers.trails import findTrails

    rootNode = Node('rootNode')

    graph = Graph(rootNode)
    graph.add_node('node1', 'rootNode')
    graph.add_node('node2', 'rootNode')
    graph.add_node('node3', 'node1')
    graph.add_edge('node2', 'node3')


    ftrails = findTrails(rootNode, 'rootNode', 'node3')
    ftrails.print()

    # =============== OUTPUT ===============
    [['rootNode', 'node1', 'node3'], ['rootNode', 'node2', 'node3']]
