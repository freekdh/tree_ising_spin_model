from dataclasses import dataclass
from typing import Iterable
from networkx import DiGraph

@dataclass(frozen=True)
class IsingTreeProblem:
    """
    This class represents the ising tree problem to be solved.
    """

    directed_graph: DiGraph

    def get_n_nodes(self):
        return self.directed_graph.number_of_nodes()

    def get_n_weights(self):
        """
        Return all the weights in the directed graph (including nodes and edges)
        """
        return len(set(self.get_nodes_with_nonzero_weights())) + len(set(self.get_edges_with_nonzero_weights()))

    def get_nodes_with_nonzero_weights(self) -> Iterable:
        for node in self.directed_graph.nodes:
            print(node)
        print(self.directed_graph.edges)
        return (node for node in self.directed_graph.nodes if node["weight"] != 0)

    def get_edges_with_nonzero_weights(self) -> Iterable:
        return (edge for edge in self.directed_graph.edges if edge["weight"] != 0)

