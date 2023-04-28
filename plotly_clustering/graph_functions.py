from networkx import *
from collections import defaultdict

# Некорректная реализация
# Отрабатывает быстро, но результат не оптимален, хотя внешне похож на настоящий алгоритм Прима
def get_spanning_trees(graph):
	edges, nodes = [], []
	weight_bias = defaultdict(lambda: 0)

	for node in graph.nodes:
		nodes.append(node)
		connected_edges = graph.edges(node)

		min_edge = min(connected_edges, key = lambda x: graph.get_edge_data(*x)["weight"] + weight_bias[x[0]] + weight_bias[x[1]])
		min_weight = graph.get_edge_data(*min_edge)["weight"]

		weight_bias[node] = 10**6

		edges.append((*min_edge, min_weight))

	G = Graph()
	G.add_weighted_edges_from(edges)
	G.add_nodes_from(nodes)

	return G

# Кластеризовать на n кластеров
def split_to_forests(graph, n=3):
	#G2 = get_spanning_trees(graph)
	G2 = minimum_spanning_tree(graph, algorithm="prim")

	for i in range(n - 1):
		max_edge = max(G2.edges, key = lambda x: G2.get_edge_data(*x)["weight"])
		G2.remove_edge(*max_edge)

	return [G2.subgraph(c) for c in connected_components(G2)]

def split_nodes_edges(nodes, edges, n=3):
	G = Graph()
	G.add_weighted_edges_from(edges)
	G.add_nodes_from(nodes)

	return split_to_forests(G, n)
