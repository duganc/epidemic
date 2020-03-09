import unittest
from src.graph import Node, Edge, Graph, PartitionGenerator, DiscreteProbabilitySpace

class GraphTests(unittest.TestCase):

	def test_partition_generator_generates(self):
		nodes = {Node(i) for i in range(0, 5)}
		size_space = DiscreteProbabilitySpace({1: 0.5, 2: 0.5})
		generator = PartitionGenerator(nodes)
		self.assertTrue(isinstance(generator, PartitionGenerator))

		graph = generator.generate(size_space, 0.5)
		self.assertTrue(isinstance(graph, Graph))
		self.assertEqual(graph.get_nodes(), nodes)

	def test_graph_constructs(self):
		graph = Graph()
		self.assertTrue(isinstance(graph, Graph))

	def test_discrete_probability_space_constructs(self):
		weights = {
			0: 1,
			1: 2,
			-5: 3
		}
		space = DiscreteProbabilitySpace(weights)
		self.assertAlmostEqual(space.get_p(0), 1/6)
		self.assertAlmostEqual(space.get_p(1), 2/6)
		self.assertAlmostEqual(space.get_p(-5), 3/6)
		self.assertAlmostEqual(space.get_p(99), 0)

	def test_node_constructs(self):

		node = Node("abc")
		self.assertEqual(node.get_id(), "abc")

	def test_edge_constructs(self):

		a = Node(1)
		b = Node(2)
		w = 0.98
		edge = Edge(b, a, w)
		self.assertEqual(edge.get_a(), a)
		self.assertEqual(edge.get_b(), b)

