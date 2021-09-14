import logging
import random
from abc import ABC, abstractmethod
from os import path
from typing import Dict, List, Tuple

import networkx
from networkx import DiGraph
from networkx.algorithms.tree.coding import from_nested_tuple
from networkx.classes.graph import Graph
from networkx.convert import from_edgelist

from tree_ising.problem import IsingTreeProblem

logger = logging.getLogger(__name__)


class ProblemLoader(ABC):
    """Base class for loading the ising tree problems."""

    def __init__(self, seed: int = None):
        """If root node is not None, this will be used as root node.

        Otherwise we draw a random root node.
        """
        if seed:
            random.seed(seed)

    @abstractmethod
    def load_problem(self, file_path: str) -> IsingTreeProblem:
        pass

    def _get_random_root_node(self, nodes: List[int]) -> int:
        return random.choice(nodes)


class ProblemLoaderFromFile(ProblemLoader):
    def load_problem(self, file_path: str, root_node: int = None) -> IsingTreeProblem:
        """Assuming the problem file:

        - A comment line start with a lower case c and may appear anywhere
        - The problem line starts with a p and appears before the data lines.
        It containts three fields (test_name, #spins, #weights) and separated by
        at least one space. The number of weights is equal to the number of data lines.
        - Data lines contain three fields (u,v,weight). The weights are integers.

        If root node is None, a random one is chosen.
        """
        assert path.isfile(file_path)

        graph, weights = self._get_graph_and_weights_from_file(file_path)
        assert networkx.is_tree(
            graph
        ), f"The graph defined in file {file_path} is not a tree"

        if root_node is None:
            root_node = self._get_random_root_node(nodes=list(graph.nodes))

        logging.info(f"chosen '{root_node}'' as root node")

        directed_graph = networkx.bfs_tree(graph, root_node)

        self._add_weights_to_graph(directed_graph, weights)

        return IsingTreeProblem(directed_graph=directed_graph, root_node=root_node)

    def _get_graph_and_weights_from_file(self, file_path: str) -> Tuple[Graph, List]:
        with open(file_path) as input_file:
            for line in input_file:
                if line.startswith("p"):
                    _, file_name, n_spins, n_weights = line.strip().split(" ")
                    n_spins, n_weights = int(n_spins), int(n_weights)
                    logger.info(f"loading problem {file_name}")
                    break

            data_lines = list(
                tuple(map(int, data_line.strip().split(" ")))
                for data_line in input_file
            )

            graph = Graph((data_line[:2] for data_line in data_lines))
            graph.remove_edges_from(networkx.selfloop_edges(graph))

        return (graph, data_lines)

    def _add_weights_to_graph(self, directed_graph: DiGraph, weights):
        # Default all spins have a weight of 0
        for node in directed_graph.nodes:
            directed_graph.nodes[node]["weight"] = 0

        # Assign weights to directed graph
        for weight_data in weights:
            node_i, node_j, weight = weight_data
            if node_i == node_j:
                directed_graph.nodes[node_i]["weight"] = weight
            else:
                # The weight is independent of the direction of the edge.
                try:
                    directed_graph.edges[(node_i, node_j)]["weight"] = weight
                except KeyError:
                    directed_graph.edges[(node_j, node_i)]["weight"] = weight
