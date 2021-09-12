from tree_ising.problem import IsingTreeProblem
from abc import ABC, abstractmethod
from os import path
from networkx import DiGraph


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
        - The problem line starts with a p and appears before the data lines.
        It containts three fields (test_name, #spins, #weights) and separated by
        at least one space. The number of weights is equal to the number of data lines.
        - Data lines contain three fields (u,v,weight). The weights are integers.
        """
        assert path.isfile(file_path)

        directed_graph = DiGraph()
        with open(file_path) as input_file:
            for line in input_file:
                if line.startswith("p"):
                    file_name = line
                    n_spins = line
                    n_weights = line
                    break
            for data_line in input_file:
                node_i, node_j, weight = data_line.split(" ")
                directed_graph.add_edge(node_i, node_j, weight=weight)

        return IsingTreeProblem(directed_graph=directed_graph)
