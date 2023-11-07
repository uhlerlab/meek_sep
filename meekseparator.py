import random
import graphical_models as gm
import network as nx
from networkx.algorithms.tree.decomposition import junction_tree
from networkx.algorithms.components.connected import connected_components


def find_meek_sep(dag: gm.DAG) -> list:
	"""
		return the 1/2-meek separator of the essential graph of dag
		requirement: dag is chordal and connected
	"""

	ug = nx.Graph()
	ug.add_nodes_from(dag.nodes)
	ug.add_edges_from(dag.arcs)
	K = find_clique_sep(ug)

	I = []
	ess_graph = dag.cpdag() # save compute
	while K:
		u = random.sample(K, 1)[0]
		I.append(set(u))
		I_ess_graph = dag.interventional_cpdag(I, ess_graph)

		ug = nx.Graph()
		ug.add_nodes_from(I_ess_graph.nodes)
		ug.add_edges_from(I_ess_graph.edges)
		H = sorted(connected_components(ug), key=len)[-1]
		if len(H) <= dag.nnodes / 2:
			break
		if H.intersection(dag.descendants_of(u)):
			K = K.intersection(dag.children_of(u))
		else:
			K = K.intersection(dag.parents_of(u))

	return I


def find_clique_sep(ug: nx.Graph):
	"""
		return the 1/2-clique separator of an undirected graph using clique tree algorithm
		requirement: ug is chordal and connected
	"""
	clique_tree = junction_tree(ug)
	
	best_clique = None
	best_score = ug.degree
	for node in clique_tree.nodes(data='type'):
		if node[1] == 'clique':
			tmp = ug.copy()
			tmp.remove_nodes_from(node[0])
			score = len(max(connected_components(tmp), key=len))
			if score < best_score:
				best_clique = sep
				best_score = score

	return best_clique
