from functools import reduce
from pyvis.network import Network
import networkx as nx
import random
from copy import deepcopy

class PartitionGenerator:

	def __init__(self, nodes, size_space, weight, allow_remainder=True):
		assert type(nodes) == set
		assert all(isinstance(node, Node) for node in nodes)
		assert isinstance(size_space, DiscreteProbabilitySpace)
		assert size_space.are_keys_positive_ints()
		assert type(weight) == float
		assert 0.0 <= weight <= 1.0
		assert type(allow_remainder) == bool

		self._nodes = nodes
		self._size_space = size_space
		self._weight = weight
		self._allow_remainder = allow_remainder

	def generate(self):
		
		nodes_left = self.get_nodes()
		graph = Graph(self.get_nodes())

		while len(nodes_left) > 0:
			n = self._size_space.draw()
			assert type(n) == int
			assert n > 0
			cluster = set(random.sample(nodes_left, min(n, len(nodes_left))))
			graph.add_complete_subgraph(cluster, self._weight)
			nodes_left = nodes_left - cluster

		return graph

	def get_nodes(self):

		return {node.copy() for node in self._nodes}

class Graph:

	def __init__(self, nodes = None, edges = None):
		if nodes is None:
			nodes = set()
		if edges is None:
			edges = set()
		assert type(nodes) == set
		assert all(isinstance(node, Node) for node in nodes)
		assert type(edges) == set
		assert all(isinstance(edge, Edge) for edge in edges)
		self._nodes = nodes
		self._edges = edges
		self._edge_color = "white"

	def get_nodes(self):
		return deepcopy(self._nodes)

	def get_edges(self):
		return deepcopy(self._edges)

	def get_weights(self):
		return {(e.get_a(), e.get_b()): e.get_weight() for e in self._edges}

	def add_edge(self, edge):
		assert isinstance(edge, Edge)

		self._edges.add(edge)

	def set_edge_color(self, color):
		self._edge_color = color

	def add_complete_subgraph(self, nodes, weight):
		assert type(nodes) in (list, set)
		assert all(isinstance(node, Node) for node in nodes)
		assert all(node in self._nodes for node in nodes)
		assert type(weight) == float
		assert 0.0 <= weight <= 1.0

		nodes = list(nodes)
		n = len(nodes)

		for i in range(0, n):
			for j in range(i + 1, n):
				self.add_edge(Edge(nodes[i], nodes[j], weight))

	@staticmethod
	def aggregate(left, right):
		assert isinstance(left, Graph)
		assert isinstance(right, Graph)
		assert left._nodes == right._nodes

		nodes = left.get_nodes()
		weights = left.get_weights()
		right_weights = right.get_weights()

		for e, w in right_weights.items():
			if e in weights.keys():
				weights[e] = 1 - (1 - weights[e])*(1 - w) # p(False -> True) = 1 - p(doesn't get it) = 1 - p(doesn't get it from first)*p(doesn't get it from second)
			else:
				weights[e] = w

		edges = {Edge(a, b, w) for ((a, b), w) in weights.items()}

		return Graph(nodes=nodes, edges=edges)


	def to_pyvis(self):
		network = Network(height="750px", width="100%", bgcolor="#222222", font_color="white")
		for node in self._nodes:
			network.add_node(node.get_id())

		for edge in self._edges:
			network.add_edge(
				edge.get_a().get_id(),
				edge.get_b().get_id(),
				color=self._edge_color,
				weight=edge.get_weight(),
				label="{label}".format(label=round(edge.get_weight(), 2))
			)

		return network


class DiscreteProbabilitySpace:

	def __init__(self, d):
		assert type(d) == dict
		assert all((type(v) in {int, float}) for (k, v) in d.items())

		weights = self._compute_weights(d)
		self._weights = weights

	def get_p(self, key):
		if key in self._weights.keys():
			return self._weights[key]
		else:
			return 0.0

	def draw(self):
		p = random.random()
		so_far = 0.0
		for k, v in self._weights.items():
			so_far += v
			if p < so_far:
				return k

		assert False

	def are_keys_positive_ints(self):
		return self.keys_of_instance and all(k >= 0 for k in self._weights.keys())

	def keys_of_instance(self, t):
		return all(isinstance(k, t) for k in self._weights.keys())

	def _compute_weights(self, d):

		total = float(reduce(lambda x, y: x + y, [v for (k, v) in d.items()]))
		assert total > 0

		return {k: (v/total) for (k, v) in d.items()}

class Node:

	def __init__(self, id):
		self._id = id

	def __str__(self):
		return 'Node({})'.format(self._id)

	def __repr__(self):
		return str(self)

	def __eq__(self, other):
		if not isinstance(other, Node):
			return False

		return self._id == other._id

	def __lt__(self, other):
		return self._id < other._id

	def __hash__(self):
		return hash(self._id)

	def __neq__(self, other):
		return not self == other

	def get_id(self):
		return self._id

	def copy(self):
		return Node(self._id)

class Edge:

	def __init__(self, a, b, weight):
		assert isinstance(a, Node)
		assert isinstance(b, Node)
		assert a != b
		assert type(weight) == float
		assert 0.0 <= weight <= 1.0

		if b < a:
			swap = b
			b = a
			a = swap

		self._a = a
		self._b = b
		self._weight = weight

	def __str__(self):
		return 'Edge({}, {}, {})'.format(self._a, self._b, self._weight)

	def __repr__(self):
		return str(self)

	def __eq__(self, other):
		if not isinstance(other, Edge):
			return False

		return (self._a == other._b) or (self._b == other._a)

	def __hash__(self):
		return hash((self._a, self._b))

	def __neq__(self, other):
		return not self == other

	def get_a(self):
		return self._a.copy()

	def get_b(self):
		return self._b.copy()

	def get_weight(self):
		return self._weight

