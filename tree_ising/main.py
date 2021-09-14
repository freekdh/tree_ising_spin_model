import logging
import sys
from dataclasses import dataclass
from functools import lru_cache

from networkx import topological_sort
from networkx.classes.digraph import DiGraph

from tree_ising.problem import IsingTreeProblem
from tree_ising.problem_loader import ProblemLoaderFromFile

logger = logging.getLogger(__name__)


class IsRootSpinException(Exception):
    pass


@dataclass
class SubConfiguration:
    value: int
    spin_formation: str


@lru_cache(maxsize=None)
def min_energy_configuration_subtree(
    focal_spin: int, parent_spin_value: int, directed_graph: DiGraph
):
    """Need to provide focal spin and parent spin value.

    Does not work on root node as it does not have a parent spin.
    """

    logger.info(
        f"evaluating min energy configuration subtree with spin:{focal_spin} and parent spin value:{parent_spin_value}"
    )

    def get_min_energy_given_focal_and_parent_spin_value(
        focal_spin_value: int, parent_spin: int, parent_spin_value: int
    ):
        min_energy_subtree_given_focal_spin_value = sum(
            min_energy_configuration_subtree(
                focal_spin=to_spin,
                parent_spin_value=focal_spin_value,
                directed_graph=directed_graph,
            )
            for _, to_spin in directed_graph.out_edges(focal_spin)
        )

        focal_weight = directed_graph.nodes[focal_spin]["weight"]
        focal_spin_value_contribution = focal_spin_value * focal_weight

        parent_to_focal_weight = directed_graph.edges[(parent_spin, focal_spin)][
            "weight"
        ]
        parent_spin_value_contribution = (
            focal_spin_value * parent_spin_value * parent_to_focal_weight
        )

        return (
            min_energy_subtree_given_focal_spin_value
            + focal_spin_value_contribution
            + parent_spin_value_contribution
        )

    if predecessor := list(directed_graph.predecessors(focal_spin)):
        assert len(predecessor) == 1
        parent_spin = predecessor[0]
        result = min(
            get_min_energy_given_focal_and_parent_spin_value(
                focal_spin_value=focal_spin_value,
                parent_spin=parent_spin,
                parent_spin_value=parent_spin_value,
            )
            for focal_spin_value in {-1, 1}
        )
        logger.info(f"Result is: {result}")
        return result
    else:
        raise IsRootSpinException(f"{focal_spin} is a root node.")


@lru_cache(maxsize=None)
def min_energy_subtree(focal_spin: int, parent_spin: int):
    raise NotImplementedError


def solve_ising_problem(ising_problem: IsingTreeProblem):
    root_node = ising_problem.root_node

    def get_min_energy_configuration_given_root_node_value(root_node_value):
        child_spin_contribution = sum(
            min_energy_configuration_subtree(
                focal_spin=to_spin,
                parent_spin_value=root_node_value,
                directed_graph=ising_problem.directed_graph,
            )
            for _, to_spin in ising_problem.directed_graph.out_edges(root_node)
        )

        root_weight = ising_problem.directed_graph.nodes[root_node]["weight"]
        root_spin_contribution = root_node_value * root_weight

        return child_spin_contribution + root_spin_contribution

    return min(
        get_min_energy_configuration_given_root_node_value(root_node_value)
        for root_node_value in {-1, 1}
    )


if __name__ == "__main__":

    # Set the logging module to stdout

    # logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    problem_loader = ProblemLoaderFromFile()
    ising_problem = problem_loader.load_problem(
        file_path="tests/test_problems/input_test_problem.txt", root_node=0
    )

    print(solve_ising_problem(ising_problem))
