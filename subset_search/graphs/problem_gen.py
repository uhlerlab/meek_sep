import numpy as np
from .DAG_gen import *


class subset_search(object):

	def __init__(self, nnodes, sampler = 'gnp_tree', hop=1):
		
		type_graph = {
			'gnp_tree': gnp_tree,
			'random': random_graph,
			'line': line_graph,
			'tree': tree_graph,
			'complete': complete_graph,
			'shanmugam': shanmugam_random_chordal,
			'd_tree': random_directed_tree,
			'clique_tree': tree_of_cliques,
			'barbasi_albert': barabasi_albert_graph
			}.get(sampler, None)
		assert type_graph, "unsupported sampler!"
		self.DAG = type_graph(nnodes)

		# sample target edges based on the hop model in choo & shiragur 22
		center = random.sample(list(self.DAG.nodes), 1)
		subgraph_nodes = set(center)
		for _ in range(hop):
			for v in subgraph_nodes.copy():
				subgraph_nodes.update(self.DAG.neighbors_of(v))
		self.target_edges = []
		for u,v in self.DAG.arcs:
			if u in subgraph_nodes and v in subgraph_nodes:
				self.target_edges.append((u,v))

		self.reset()


	def intervene(self, targets_list):
		self.ess_graph = self.DAG.interventional_cpdag(targets_list, cpdag=self.ess_graph)
		self.unsolved_target_edges = [
			(u,v) for u,v in self.unsolved_target_edges if (u,v) not in self.ess_graph.arcs
		]


	def reset(self):
		self.ess_graph = self.DAG.cpdag()
		self.unsolved_target_edges = [
			(u,v) for u,v in self.target_edges if (u,v) not in self.ess_graph.arcs
			]
