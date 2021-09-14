import logging
import sys
from dataclasses import dataclass
from functools import lru_cache, total_ordering
from typing import Dict

from networkx import topological_sort
from networkx.classes.digraph import DiGraph

from tree_ising.problem import IsingTreeProblem
from tree_ising.problem_loader import ProblemLoaderFromFile

logger = logging.getLogger(__name__)


class IsRootSpinException(Exception):
    pass


@total_ordering
@dataclass
class PartialConfiguration:
    energy: int
    spin_assignment: Dict[int, int]

    def __eq__(self, other):
        assert set(self.spin_assignment.keys()) == set(other.spin_assignment.keys())
        return self.energy == other.energy

    def __lt__(self, other):
        assert set(self.spin_assignment.keys()) == set(other.spin_assignment.keys())
        return self.energy < other.energy

    def __add__(self, other):
        for intersecting_spin in set(self.spin_assignment.keys()).intersection(
            set(other.spin_assignment.keys())
        ):
            assert (
                self.spin_assignment[intersecting_spin]
                == other.spin_assignment[intersecting_spin]
            )

        return PartialConfiguration(
            energy=self.energy + other.energy,
            spin_assignment={**self.spin_assignment, **other.spin_assignment},
        )


@lru_cache(maxsize=None)
def min_energy_subtree(
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
            (
                min_energy_subtree(
                    focal_spin=to_spin,
                    parent_spin_value=focal_spin_value,
                    directed_graph=directed_graph,
                )
                for _, to_spin in directed_graph.out_edges(focal_spin)
            ),
            PartialConfiguration(energy=0, spin_assignment=dict()),
        )

        focal_weight = directed_graph.nodes[focal_spin]["weight"]
        focal_spin_value_contribution = focal_spin_value * focal_weight

        parent_to_focal_weight = directed_graph.edges[(parent_spin, focal_spin)][
            "weight"
        ]
        parent_spin_value_contribution = (
            focal_spin_value * parent_spin_value * parent_to_focal_weight
        )

        min_energy = (
            min_energy_subtree_given_focal_spin_value.energy
            + focal_spin_value_contribution
            + parent_spin_value_contribution
        )
        spin_assignment = {
            **min_energy_subtree_given_focal_spin_value.spin_assignment,
            **{focal_spin: focal_spin_value, parent_spin: parent_spin_value},
        }

        return PartialConfiguration(energy=min_energy, spin_assignment=spin_assignment)

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


def solve_ising_problem(ising_problem: IsingTreeProblem):
    root_node = ising_problem.root_node

    def get_min_energy_configuration_given_root_node_value(root_node_value):
        child_spin_contribution = sum(
            (
                min_energy_subtree(
                    focal_spin=to_spin,
                    parent_spin_value=root_node_value,
                    directed_graph=ising_problem.directed_graph,
                )
                for _, to_spin in ising_problem.directed_graph.out_edges(root_node)
            ),
            PartialConfiguration(energy=0, spin_assignment=dict()),
        )
        root_weight = ising_problem.directed_graph.nodes[root_node]["weight"]
        root_spin_contribution = root_node_value * root_weight

        child_spin_contribution.energy += root_spin_contribution

        return child_spin_contribution

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

    solution_configuration = solve_ising_problem(ising_problem)

    from tree_ising.output_handler import FileOutputHandler

    file_output_handler = FileOutputHandler(file_path="output.txt")
    file_output_handler.handle_configuration(
        solution_configuration=solution_configuration
    )
