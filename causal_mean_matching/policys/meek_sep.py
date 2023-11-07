from itertools import permutations
import random
import graphical_models as gm
import networkx as nx
from networkx.algorithms.tree.decomposition import junction_tree
from networkx.algorithms.components.connected import connected_components

from graphs import mean_match


def meek_sep_policy(p: mean_match, onebyone=False) -> list:
	"""
	if upstream_most:
		pick upstream_most
	else:
		pick from partial_upstream_most using meek sep
	"""

	int_list = []
	int_buffer = []
	while not p.solved:
		upstream_most, partial_upstream_most = p.remained_upstream_most      
		if upstream_most:
			targets = set(random.sample(list(upstream_most), 1))
		else:
			if int_buffer and ~onebyone:
				targets = int_buffer.pop()
			else:
				if partial_upstream_most:
					top_chain_components = p.DAG.induced_subgraph(partial_upstream_most)
					ug = nx.Graph()
					ug.add_nodes_from(top_chain_components.nodes)
					ug.add_edges_from(top_chain_components.arcs)
					H = list(connected_components(ug))[0]
					top_chain_component = p.DAG.induced_subgraph(H)
					int_buffer = find_meek_sep(top_chain_component)
					targets = int_buffer.pop()
				else:
					print("Error: p should be solved!")

		p.intervene(targets)
		int_list.append(targets)

	return int_list



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
		u = random.sample(list(K), 1)[0]
		I.append({u})
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
	
	best_clique = set()
	best_score = len(ug.nodes)
	for node in clique_tree.nodes(data='type'):
		if node[1] == 'clique':
			tmp = ug.copy()
			tmp.remove_nodes_from(node[0])
			if len(tmp.nodes):
				score = len(max(connected_components(tmp), key=len))
			else:
				score = 0
			if score < best_score:
				best_clique = set(node[0])
				best_score = score

	return best_clique
