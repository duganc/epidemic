import argparse
from graph import PartitionGenerator, Graph, Node, DiscreteProbabilitySpace

parser = argparse.ArgumentParser(description='Visualize a graph of an epidemic given inputs')
parser.add_argument('n_nodes', type=int,
                    help='Number of nodes in the graph')
# parser.add_argument('--sum', dest='accumulate', action='store_const',
#                     const=sum, default=max,
#                     help='sum the integers (default: find the max)')

args = parser.parse_args()
nodes = {Node(i) for i in range(0, args.n_nodes)}
size_space = DiscreteProbabilitySpace({1: 0.5, 2: 0.2, 3: 0.1, 4: 0.1, 5: 0.05, 6: 0.05})
generator = PartitionGenerator(nodes, size_space, 1.0/3.0, allow_remainder=True)
graph_1 = generator.generate()
graph_2 = generator.generate()
graph_3 = generator.generate()

graph = Graph.aggregate(graph_1, graph_2)
graph = Graph.aggregate(graph, graph_3)
pyvis_graph = graph.to_pyvis()

pyvis_graph.show_buttons(filter_=['physics'])
pyvis_graph.show("graph.html")