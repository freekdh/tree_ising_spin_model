from tree_ising.problem import IsingTreeProblem
from abc import ABC, abstractmethod
from os import path
from networkx import DiGraph, read_weighted_edgelist, selfloop_edges

class ProblemLoader(ABC):
    """
    Base class for loading the ising tree problems
    """

    @abstractmethod
    def load_problem(self, file_path: str) -> IsingTreeProblem:
        pass


class ProblemLoaderFromFile(ProblemLoader):
    def load_problem(self, file_path: str) -> IsingTreeProblem:
        """
        Assuming the problem file:
        - A comment line start with a lower case c and may appear anywhere
        - The problem line starts with a c followed by a p and appears before the data lines.
        It containts three fields (test_name, #spins, #weights) and separated by
        at least one space. The number of weights is equal to the number of data lines.
        - Data lines contain three fields (u,v,weight). The weights are integers.
        """


        assert path.isfile(file_path)
        directed_graph = read_weighted_edgelist(file_path, comments="c", delimiter=" ", create_using=DiGraph, nodetype=int)

        #Selfloops are created instead of assigning the weights to the nodes as attributes.
        self_loop_edges = selfloop_edges(directed_graph)
        for self_loop_edge in self_loop_edges:
            node = self_loop_edge[0]
            weight = directed_graph.get_edge_data(*self_loop_edge)["weight"]
            directed_graph[node]["weight"] = weight
        directed_graph.remove_edges_from(self_loop_edges)

        return IsingTreeProblem(directed_graph=directed_graph)
