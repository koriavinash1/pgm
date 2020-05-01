pgm\.representation package
===========================

Subpackages
-----------

.. toctree::

    pgm.representation.algorithms

Submodules
----------

pgm\.representation\.BN module
------------------------------

.. automodule:: pgm.representation.BN
    :members:
    :undoc-members:
    :show-inheritance:

pgm\.representation\.LinkedListBN module
----------------------------------------

.. automodule:: pgm.representation.LinkedListBN
    :members:
    :undoc-members:
    :show-inheritance:

pgm\.representation\.LinkedListMN module
----------------------------------------

.. automodule:: pgm.representation.LinkedListMN
    :members:
    :undoc-members:
    :show-inheritance:

pgm\.representation\.MN module
------------------------------

.. automodule:: pgm.representation.MN
    :members:
    :undoc-members:
    :show-inheritance:


Module contents
---------------

.. automodule:: pgm.representation
    :members:
    :undoc-members:
    :show-inheritance:

Usage
-----

1. LinkedList BN representation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python
    from pgm.helpers.common import Node
    from pgm.representation.LinkedListBN import Graph

    rootNode = Node('rootNode')

    graph = Graph(rootNode)
    graph.add_node('node1', ['rootNode'])
    graph.add_node('node2', ['rootNode'])
    graph.add_node('node3', ['node1', 'node2'])
    graph.add_edge('rootNode', 'node3')
    graph.print(rootNode)

    # =============== OUTPUT ===============
    node: rootNode, children: ['node1', 'node2', 'node3'], parents: []
    node: node1, children: ['node3'], parents: ['rootNode']
    node: node2, children: ['node3'], parents: ['rootNode']
    node: node3, children: [], parents: ['node1', 'node2', 'rootNode']


2. LinkedList  MN representation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python
    from pgm.helpers.common import Node
    from pgm.representation.LinkedListMN import Graph

    rootNode = Node('rootNode')

    graph = Graph(rootNode)
    graph.add_node('node1', ['rootNode'])
    graph.add_node('node2', ['rootNode', 'node1'])
    graph.add_node('node3', ['node1'])
    graph.add_edge('node2', 'node3')
    graph.print(rootNode)

    # =============== OUTPUT ===============
    node: rootNode, nbrs: ['node1', 'node2']
    node: node1, nbrs: ['rootNode', 'node2', 'node3']
    node: node2, nbrs: ['rootNode', 'node1', 'node3']
    node: node3, nbrs: ['node1', 'node2']


3. Set Local (conditional) Distribution
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Set conditional distribution per node:

In case of BN 
.. math::`\mathbb{P}(node~|~Par_{node})`

.. code:: python
    from pgm.helpers.common import Node
    from pgm.representation.LinkedListBN import Graph

    rootNode = Node('rootNode')
    rootNode.values = [0,1,2]
    rootNode.set_distribution(probability=None)
    # you can set probability to some flag to directly feed values
    # else you need to manually enter conditional probabilities

    graph = Graph(rootNode)
    graph.add_node('node1', ['rootNode'])
    graph.print(rootNode)

    node1 = graph.get_node('node1')
    node1.values=[1, 2, 3]
    node1.set_distribution(probability=None)



In case of MN
.. math::`\mathbb{P}(node~|~Nbr_{node})`

It's very similar to the example of BN showen above

.. code:: python
    from pgm.helpers.common import Node
    from pgm.representation.LinkedListMN import Graph

    rootNode = Node('rootNode')
    rootNode.values = [0,1,2]
    rootNode.set_distribution()


    graph = Graph(rootNode)
    graph.add_node('node1', ['rootNode'])
    graph.print(rootNode)

    node1 = graph.get_node('node1')
    node1.values=[1, 2, 3]
    node1.set_distribution()


4. Caculate Conditional
~~~~~~~~~~~~~~~~~~~~
.. math::`\mathbb{P}(nodeB ~|~nodeA) = \frac{mathbb{P}(nodeB, nodeA)}{nodeA}`

Not Implemented yet


5. Caculate Marginal
~~~~~~~~~~~~~~~~~~~~
.. math::`\mathbb{P}(nodeB ~|~somenodes) = \sum_{nodeA}\mathbb{P}(nodeA, nodeB ~|~somenodes)`

Not Implemented yet
