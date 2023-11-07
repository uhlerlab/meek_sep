from itertools import permutations
import random
import graphical_models as gm
import networkx as nx
from networkx.algorithms.tree.decomposition import junction_tree
from networkx.algorithms.components.connected import connected_components

from graphs import subset_search


def meek_sep_policy(p: subset_search, onebyone=False, subset=False) -> list:
	"""
		run meek separator on a subset search problem
	"""
	if subset:
		subset_nodes = set()
		for edge in p.target_edges:
			subset_nodes.update(edge)

	I_sol = []
	while p.unsolved_target_edges:
		ug = nx.Graph()
		ug.add_nodes_from(p.ess_graph.nodes)
		ug.add_edges_from(p.ess_graph.edges)
		CCs = connected_components(ug)
		I_s = []
		for H in CCs:
			if set(permutations(H, 2)).intersection(set(p.unsolved_target_edges)) and len(H) >= 2:
				sub_dag = p.DAG.induced_subgraph(H)				
				I = find_meek_sep(sub_dag)
				if onebyone:
					if subset:
						if len([i for i in I if i in subset_nodes])>0: 
							I_s.extend(random.sample([i for i in I if i in subset_nodes],1))
						else:
							I_s.extend(random.sample(I,1))
					else:
						I_s.extend(random.sample(I,1))
				else:
					if subset:
						if len([i for i in I if i in subset_nodes])>0:
							I_s.extend([i for i in I if i in subset_nodes])
						else:
							I_s.extend(I)
					else:
						I_s.extend(I)
		I_sol.extend(I_s)
		p.intervene(I_sol)
	return I_sol


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
