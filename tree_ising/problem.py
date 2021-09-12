from dataclasses import dataclass
from typing import Iterable
from networkx import DiGraph


@dataclass(frozen=True)
class IsingTreeProblem:
    """
    This class represents the ising tree problem to be solved.
    """

    directed_graph: DiGraph
    root_node: int

    def get_n_nodes(self):
        return self.directed_graph.number_of_nodes()

    def get_n_weights(self):
        """
        Return all the weights in the directed graph (including nodes and edges)
        """
        return (
            len(set(self.get_nodes_with_nonzero_weights()))
            + self.directed_graph.number_of_edges()
        )

    def get_nodes_with_nonzero_weights(self) -> Iterable:
        return (
            node
            for node, data in self.directed_graph.nodes(data=True)
            if data["weight"] != 0
        )
