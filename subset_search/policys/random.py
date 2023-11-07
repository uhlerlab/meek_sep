import random
import graphical_models as gm
import networkx as nx
from networkx.algorithms.tree.decomposition import junction_tree
from networkx.algorithms.components.connected import connected_components

from graphs import subset_search


def random_policy(p: subset_search) -> list:
	"""
		run meek separator on a subset search problem
	"""
	I_sol = []
	while p.unsolved_target_edges:
		ug = nx.Graph()
		ug.add_nodes_from(p.ess_graph.nodes)
		ug.add_edges_from(p.ess_graph.edges)
		non_dominate_nodes = [{i} for i in ug.nodes if len(list(ug.neighbors(i)))!=0]
		I_s = random.sample(non_dominate_nodes,1)
		I_sol.extend(I_s)
		p.intervene(I_sol)
	return I_sol


