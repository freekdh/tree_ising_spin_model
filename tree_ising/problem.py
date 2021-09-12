from dataclasses import dataclass
from networkx import DiGraph


@dataclass(frozen=True)
class IsingTreeProblem:
    """
    This class represents the ising tree problem to be solved.
    """

    directed_graph: DiGraph
